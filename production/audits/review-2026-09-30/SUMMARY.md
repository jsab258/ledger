# Independent review of 30 September: what is still wrong with the week

An independent review, 30 September 2026, of the route through ordinary play that was wired today, and of the town's fixes. It was done by reading the code, then by running small proofs of the most serious faults. That second step was run with Jafar's approval, once this machine had room for .NET.

The town's own tests pass here, as on GitHub: all 37 checks. That clears nothing below. Four of these faults are written into the very tables those tests compare against, and no test covers the game's own wiring, where most of the rest live.

The details, with the exact places in the code, are in FAULTS.md; what each proof printed is in RESULTS.md.

## The fixes of today

The fix the outside audit asked for holds: the arrangement now accepts an answer only on its own night. So do the other time fixes checked, apart from one that only a hand-edited save can reach.

## What a player would meet in the first week

"Proved" below means a small program ran the game's own code and got the fault. What only the running game can show is said beside it.

1. **The smash has the wrong witnesses.**
   - Only two fixed stand-ins can see it, and always as if in daylight: **proved**. At night light the same witness would not see him.
   - When Sheila only hears it, what she files in the town's gossip is an internal error message, not a sentence: **proved**. Whether her line to Rita's window is open in the real street needs the game.
   - Rita, behind her own window, never sees it, and an hour later "comes by" and remembers finding "Rita's window" broken.
2. **Nobody can ever report him: proved.** No witness can recognise him, because everyone is treated as a stranger all week. Nobody's loyalty ever drops low enough to go to the police. So the constable never comes, whatever he does.
3. **Keeping quiet and owning up do not work on the real deed: proved.** The game looks for the story under a different name from the one it files.
4. **The town treats a sound or a shape as proof it was him.** DS Ellis questions whoever only heard the glass break: **proved**. Townspeople saying so to his face is from reading. (Correction: window stories alone do not bring her; she comes for talk of his nights.)
5. **DS Ellis "on Quay Street" questions most of the town: proved.** At each morning visit tried, 15 to 17 of the 36 people she asks are at the docks, the customs shed or the chapel, up to 160 metres away. Each then remembers being stopped on Quay Street.
6. **Sheila's end-of-week question can be missed for good: proved** for the town's side. The game lets her ask only between ten and twelve on the Sunday; after that, the gate stays shut.
7. **After a Continue, everything he said to people can be forgotten: proved** for the conversation program. Whether the game's early save sets it off is from reading, and depends on timing.
8. **After a Continue before the smash, nobody can see it,** only hear it (from reading).
9. **Waiting skips hours in one jump.** A warning about the detective or the constable can be missed, be false, or come after the arrest it warns of (from reading).

## Where the two versions agree and are both wrong

Four of these are written into the test tables the two versions are compared against, so the tests pass because of them:
- Ellis questioning thirty-six people at one visit;
- Ada's tea judged "left early" when he came late and stayed;
- Rita finding her own window;
- Sheila remembering her own answer as something she saw.

## Also found

Two lines in the witness bank speak of a pub and opening time, which canon's content rule forbids. Only the scripted encounter can reach them.

## What still needs the game

Three short runs of the packaged game would settle the rest:
1. One smash, with the witnesses' memories read afterwards.
2. One Continue with the conversation program starting late.
3. One Sunday played past noon before seeing Sheila.
