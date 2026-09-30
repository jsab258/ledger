# Independent review of 30 September: what is still wrong with the week

An independent review, 30 September 2026, of the route through ordinary play that was wired today, and of the town's fixes. It was done by reading the code. Nothing was run on this machine, because its disk was full and .NET could not be installed. GitHub runs the town's own tests on this branch; that result is in the pull request.

The details, with the exact places in the code, are in FAULTS.md beside this file.

## The fixes of today

The fix the outside audit asked for holds: the arrangement now accepts an answer only on its own night. So do the other time fixes checked, apart from one that only a hand-edited save can reach.

## What a player would meet in the first week

1. **The smash has the wrong witnesses.** Only two fixed stand-ins can see it, at any hour, as if in daylight. Sheila, facing the other way, "witnesses" it by ear every time. What she files in the town's gossip is an internal error message, not a sentence. Rita, behind her own window, never sees it, and an hour later "comes by" and remembers finding "Rita's window" broken.
2. **Nobody can ever report him.** No witness can recognise him, because everyone is treated as a stranger all week. Nobody's loyalty ever drops low enough to go to the police. So the constable never comes, whatever he does.
3. **Keeping quiet and owning up do not work on the real deed.** The game looks for a story under a different name from the one it files.
4. **The town treats a shape seen in the dark as proof it was him,** and says so to his face.
5. **DS Ellis "on Quay Street" questions most of the town,** people at the docks and the chapel included. Each then remembers being stopped on Quay Street.
6. **Sheila's end-of-week question can be missed for good.** The game lets her ask only between ten and twelve on the Sunday, not "the next time he talks with her" as the town's own rules say.
7. **After a Continue, everything he said to people can be forgotten.** This happens if the game saves before the conversation program has started. It depends on timing, and the start-up time has not been measured.
8. **After a Continue before the smash, nobody can see it,** only hear it.
9. **Waiting skips hours in one jump.** A warning about the detective or the constable can be missed, be false, or come after the arrest it warns of.

## Where the two versions agree and are both wrong

Four of these are written into the test tables the two versions are compared against, so the tests pass because of them:
- Ellis questioning thirty-six people at one visit;
- Ada's tea judged "left early" when he came late and stayed;
- Rita finding her own window;
- Sheila remembering her own answer as something she saw.

## Also found

Two lines in the witness bank speak of a pub and opening time, which canon's content rule forbids. Only the scripted encounter can reach them.

## What would prove them

Each fault in FAULTS.md comes with a small case that can be made into a test. The quickest three:
1. One Continue with the conversation program starting a few seconds late.
2. One smash in the packaged game, with the memories read afterwards.
3. One test of Sheila's Sunday gate.
