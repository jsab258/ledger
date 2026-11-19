Verdict: PASS WITH FIXES

Review of production/lane/JULIE-DEBT-LEDGER-RULE-2026-11-18.md, 18 Nov 2026, fresh reviewer, reading only (nothing run).

## What checks out

- RULINGS.md line 115 (D12, D20, D37, "notebook of people and events") and line 110 ("from what he saw and heard, never the true state") are real.
- canon.md line 73 "a book of uncollectable debts": real.
- PROTOTYPE-SCOPE-DRAFT.md line 85, FABLE-PROTOTYPE-NEXT-ROUND.md lines 39, 40, 50, LEDGER-SCREEN-STUDY lines 3 and 83: real and quoted fairly.
- Bundle (part-02.js): Sheila's line "the Kettlewell girl nine", the note `kn("Mickey's book of debts: ... Julie Kettlewell \xA39. Nobody can pay.","debts","debts")`, the directive "You owe Mickey's book ... Deflect, in character.", the fire note `on the fire:`, the card "nine pounds of cab fares on Mickey's slate", Julie's keepSay "Nine pounds, since the summer", Dennis's greeting "If it's about the eighty quid, I'm out." all found as quoted.
- Fare after note: `x.car.keys=!0` is set once only, in Sheila's scene, in the same statement as the note; the fare offer returns early without keys (`if(e.fare||!x.car.keys)return`), and Pauline's fare offer and the "Get in the cab" prompt also need keys. Claim holds.
- Gossip: the overheard list holds no Julie or debt line; tellings carry stories about Tom. Claim holds.
- Verdict "design silent, inferred small bug" is fair: no ruling, canon line or spec says how a debt heard from a person reaches the Ledger. No em-dashes, no italics.

## Findings

1. The "unheard Julie" slip contradicts the prototype's own stated rule. The bundle's notes say "Once he has any part of a name the whole name is shown" and "Debts in "What's open" are listed by the names in Mickey's book, and go on a person's own page only once he can put that name to the face." Sheila said "Kettlewell", so "Julie Kettlewell" follows that rule; it also applies to all five (Sheila said "Iveson", "Harrison", "young Milner", "Drewery", yet the note gives Dennis, Wayne, Darren, Lee). Fix: replace the last sentence of the Verdict with "The full names in the note follow the prototype's rule that any part of a name shows the whole name; that rule is looser than the next round's "names only once learned", so the paste line changes it on purpose, for all five debtors, not only Julie." And in "What the prototype does", first bullet, replace "The note says "Julie"; she did not." with "The note gives full names for all five; Sheila gave surnames only (the prototype's notes: any part of a name shows the whole name)."

2. The paste line names the speaker without the "once learned" test. "Julie says." shows a name Tom may not have (her greeting is only "Hiya."), which breaks "nothing he could not know". It also reads "owes Mickey's £9", which is not English. Fix: replace the example with ("Says she owes Mickey's book £9, since the summer. Julie says.", the speaker named only once learned, else as Tom knows her, such as "the young woman with the carrier bag"; the sum and the "since" only as she said them).

3. The debt topic trigger is understated. The keyword test is `/(owe|debt|the book|pay up|what'?s owed|slate)/`, and with live talk on, a model classifier can also pick topic "debt (money owed)" from any line. Fix: in the second bullet replace "a typed line with "owe", "debt" or "slate" gives the debt topic" with "a typed line matching owe, debt, the book, pay up, what's owed or slate, or one the live classifier reads as about money owed, gives the debt topic".

4. RULINGS.md line 110 is about the ending's cost, not the Ledger in general. Fix: in the first bullet of "What the design says" write "Tom's reading of the ending's cost comes "from what he saw and heard, never the true state" (RULINGS.md line 110; the same rule by extension)".

5. The "17 Nov check" is mis-dated and mis-quoted. The verdict sits in LANE-QUEUE.md item 29, done 18 Nov 01:20 to 01:45, worded "Julie's debt shown only after Mickey's book: matches the design."; the playtest note reads "Julie's debt is not noted until Mickey's book is read." Fix: line 5 to "Lane check of 18 Nov 01:20 (LANE-QUEUE.md item 29) on the playtest note "Julie's debt is not noted until Mickey's book is read."", and in the Verdict replace "17 Nov's" with "that check's".

6. A test locks in the current behaviour and is not named. tools/lane/prototype/tests/systems2_test.py test_5b asserts no Julie note and no "Julie" on screen before Sheila's scene, citing "never shows a fact he could not know". Fix: add to "Note for the main session to decide": "If accepted, systems2_test.py test_5b must change: before Sheila's scene a heard claim from Julie may show; the book's entry may not."

7. A design line the note misses supports its inference. game-design/m15-the-world-speaks.md (status SPEC, M15.1) says of overheard rumours "The ledger entry becomes a side effect of having heard it", and plans ambient talk "about their own lives: debts". Fix: add a bullet under "What the design says": "M15 spec (game-design/m15-the-world-speaks.md, M15.1): a Ledger entry is a side effect of having heard something; ambient talk is planned to cover debts. About rumours of Tom, not debts told to him, so still silent on this case."
