# Julie's debt in the Ledger, 18 Nov

## The question

Lane check of 18 Nov 01:20 (LANE-QUEUE.md item 29) on the playtest note "Julie's debt is not noted until Mickey's book is read." Should hearing it otherwise note her 9.00?

## Design

- Ledger: "a notebook of people and events" (RULINGS.md line 115). Tom's reading of the ending's cost comes "from what he saw and heard, never the true state" (RULINGS.md line 110; the same rule by extension).
- Scope: "every entry traces to a noticed event or a telling" (PROTOTYPE-SCOPE-DRAFT.md line 85).
- Next round: "how Tom knows ("Darren says")"; "names only once learned" (FABLE-PROTOTYPE-NEXT-ROUND.md lines 40, 50).
- Ledger study (unruled): only what Tom "saw, heard or was told" (LEDGER-SCREEN-STUDY-2026-11-18.md line 3).
- M15 spec (game-design/m15-the-world-speaks.md, M15.1): a Ledger entry is a side effect of having heard something; ambient talk is planned to cover debts. About rumours of Tom, not debts told to him, so still silent on this case.

## Prototype

- One note only, after Sheila says "the Kettlewell girl nine" in her first scene, reading `Julie Kettlewell \xA39`. The note gives full names for all five; Sheila gave surnames only (the prototype's notes: any part of a name shows the whole name).
- Talk: a typed line matching owe, debt, the book, pay up, what's owed or slate, or one the live classifier reads as about money owed, gives the debt topic at any time; live talk is told "You owe Mickey's book £9.00 ... Deflect"; no note. Her card, which the live voice reads: "nine pounds ... on Mickey's slate".
- Her fare scene needs the car keys Sheila's scene gives, so it always follows the note.
- Gossip carries only Tom's acts.

Gap: before Sheila's scene, live talk lets Julie tell Tom unnoted.

## Verdict

Design silent. Inferred from its knowledge rule: a debt heard is a telling, noted as a heard claim apart from the book; a small bug; that check's "matches the design" was too strong. The full names in the note follow the prototype's rule that any part of a name shows the whole name; that rule is looser than the next round's "names only once learned", so the paste line changes it on purpose, for all five debtors, not only Julie.

## Fable paste line

Debts: when a debtor or anyone else tells Tom what is owed (written, or live on the game's debt directive, never an invented sum), note it once per person as a heard claim ("Says she owes Mickey's book £9, since the summer. Julie says.", the speaker named only once learned, else as Tom knows her, such as "the young woman with the carrier bag"; the sum and the "since" only as she said them); the book's entry stays separate, names only as Sheila said them ("the Kettlewell girl, £9") until learned.

## For the main session

Ledger spec: a debt heard and a debt read in Mickey's book are two entries, each with its source, never merged. If accepted, systems2_test.py test_5b must change: before Sheila's scene a heard claim from Julie may show; the book's entry may not.

## Not verified

- Nothing run. Whether the live voice volunteers the slate, or Tom meets Julie before Sheila's scene.
