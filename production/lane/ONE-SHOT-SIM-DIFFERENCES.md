# The one-shot: the prototype on the real town code, and what changed for the player

Friday 20 November 2026, the one-shot's step 4(a). The browser prototype now runs the game's own town code (the Unreal port, compiled for the browser as one-sim.wasm) through the bridge. This file lists every place the prototype's old copy of the town rules differed from the real rules, what was done about each, and what the player will notice. The measurements behind the "before" column are in tools/lane/one-sim/DIFFERENCES.md (19 November); this file is what was decided and built.

## In ten lines

1. The real town opens when a week starts or loads, and runs on the prototype's clock: its hours in the game's own order, its talk by the minute.
2. How well a witness sees Tom is now the real rule's answer (someone, a shape, a mark, a face, recognised), for everybody on the street.
3. Everything Tom does in front of somebody the real town has is told to the town, and the town's own talk carries it on.
4. Who knows what is read back from the town into the minds of the nine people both casts have, so they still say it to his face, his Ledger still learns of it and his name still climbs.
5. Who goes to the police is the real rule's answer for everybody, also for the 19 people the real cast does not have yet.
6. A blow, a wounding, a robbery or a killing seen can now bring a statement and a constable. Damage to a thing is the week's deed, as in the real game.
7. The police keep the real timetable: statements at nine the morning after, DS Ellis at nine, a constable at ten.
8. Talk cools by its kind (a remark in a day, a wounding in a week, a killing never). Memory never goes.
9. The town travels in the save. A save from before today still loads: it gets a fresh town at its clock, told what its people saw.
10. If the simulation file cannot be loaded, the game still starts and plays on the old rules, and its log says so.

## Decisions taken (they were his seven; the brief said to take them by the recommended answers)

| Decision | Taken | Why |
|---|---|---|
| 1. Names | The nine shared people keep their prototype names. The 19 the real cast lacks stay prototype people. | Names are canon and not the bridge's to mint. |
| 2. What each person thinks of him | Stays the prototype's (liking, fear, what they call him), fed from the town's facts. | Recommended; fights, debts and talk read them. |
| 3. The week | The whole game now runs past week one, so the real week's seven days fit: Sheila's question on Sunday, as DESIGN section 16 has it. The town's answer is told to it when the story asks. | The design moved to Sunday. |
| 4. The bill and the chase | The chase stays as the prototype's own scene round the town's step. The bill is money and stays the prototype's until the police builder changes it. | The design keeps chases; the real hours are in the hour's answer for the police builder to use. |
| 5. Violence and the police | A call was added. A crime seen is told to the town, reported by the town's own rule at nine, filed in the town's own police file, and a constable comes at ten on a later day if somebody recognised him. | The brief; a town where no constable comes for a wounding is not the design. |
| 6. Damage | Damage to a thing is the real week's one deed (found by people coming by, reported, a constable). The cab put into something counts as damage. A second piece of damage in the same week is kept as a crime of its own, since the real rules follow one deed. | The brief; damage by hand is built by the jobs builder with kinds marked as a deed. |
| 7. Open and decent acts | A call was added, so a fare driven, a debt struck out or the rent paid travels as an open story. | Recommended; without it good deeds stopped travelling. |

Licence: the pieces of the compiler's libraries inside one-sim.wasm are on the allowlist (item 18, "notices kept"). The credits file is written (tools/lane/prototype/ONE-SIM-CREDITS.md) and ships beside the page, with the licence texts that were read on 19 November. Four small notice files it points to could not be read in this run and are named there as owed.

## Each difference, what was done, and what the player notices

### 1. The people

- Before: 28 named people, all on the prototype's rules.
- Now: the real town has 41 people. Nine are in both (Ron, Sheila, Darren, Alison, Father Walsh, Ada, June, Rita, Hal). The other 32 of the real town have no body on this map: they talk, find things, go to the police, and are never seen. The prototype's other 19 named people have no place in the real town yet.
- What runs for the 19: they see him by the same real rule; whether they go to the police is the same real rule, asked with each one's own nerve and liking; their talk with each other and with the nine is still the prototype's own (the real town cannot be told of a telling, and has nobody by their names). This is the one place two sets of talk rules still run. It ends when the names question is settled and the cast file has them.
- The player notices: a story can now reach the police through somebody he never saw (a finder who came by). The log names them by their id, since they have no name yet.

### 2. Where people are

- Before and now: people stand where the prototype's own week puts them. The story's scenes are staged on it (Ada at her window, Sheila at the desk, Ron at the rank).
- The real town talks by its own routines all the same: who meets whom there decides how its stories travel.
- Built and switched off: a table from the cast file's 30 places to spots on this map (26 have one), and a call that says where the real routine puts each of the nine. Turning it on moves the nine by the real routine; it is off because it breaks staged scenes. It is one number in the tuning table.
- The player notices: nothing new here.

### 3. How a story travels

- Before: any two named people within reach might talk, by chance, every four game minutes; passers-by carried what they saw.
- Now: between two people the real town has, the talk is the town's own (a round every six game minutes, between people its routines put together, seeded, the same week every time). The prototype reads who holds what every six game minutes and puts it in their minds. Any talk that involves one of the 19 is still the prototype's.
- Lost for now: catching two of the nine with their heads together about him. The town says who holds a story and how many tellings from the one who saw it, not each telling as it happens. The Ledger's "saw them talking" still works for everybody else.
- The player notices: of the nine people he knows best, fewer hear of a deed (about five of nine, where it was eight), and what they hold they hold for longer.

### 4. Cooling

- Before: one fade for everything, half gone in about 20 game hours.
- Now: by kind, in game days until half gone: a remark 1, a threat 2, a blow 4, the gravest 7, a decent act 1.5, a killing never. First values. The memory itself is never removed; only how ready people are to tell it.
- The player notices: a small thing is forgotten in talk by the next evening; a blow is still being told at the week's end.

### 5. Seeing him, and knowing it was him

- Before: one clarity number and a "face score"; named above 0.36.
- Now: the real rule gives the rung. A shape to 35 m, a mark to 18 m, a face to 8 m when his face is toward them, recognised to 25 m by somebody who knows him, all scaled by the light on him. The prototype still says who has him in view at all (its own distances, light map, rain, windows and lines of sight), and it tells the rule three things: the light, whether he shows a mark, and whether his face is toward the watcher.
- What a mind keeps from the rung: recognised by somebody who knows who he is: his name. A face: "the new owner". A mark: the coat or the cab. A shape: a man. A shape in the cab still names the cab. How sure a witness is follows the rung (0.25, 0.4, 0.55, 0.8, 1).
- Kept from the prototype, as what the host tells the rule: the runner's coat with its collar up after dark and sitting in the cab both lower how well he is known.
- Kept from the prototype: a witness who saw only the coat, the cab or a face comes to tie it to him later, once they learn whose it is.
- The player notices: people who know him know his back, so turning away only fools strangers. A stranger needs his face within 8 m in good light. A dark doorway works as the design says: in it he is a shape at most from across the street.

### 6. What gives him away

- Now one list, read by the rule above as "he shows a mark": the coat, blood, dirt, a weapon in the hand, clothes wrong for the door, bruises, the car, a load. Running makes him noticed twice as fast. Each has a test row (a witness catches more with it than without).
- Blood, dirt, wrong clothes and bruises are read if the builders of those parts set them; today only the coat, the cab, the bag, a weapon out and running are set by the game.

### 7. The police

- Before: a witness who saw it plainly, was sure, not afraid and did not like him gave a statement that night; a constable came at nine; four or five hours.
- Now: at nine on the morning after, each witness goes if the real rule says so. For damage and for a wounding or worse, seeing it is enough, unless they are on his side, frightened or bought before nine, or one of those who never go. For a plain blow only the man who was hit may go. Whoever recognised him gives a statement; the rest give a description.
- A constable comes at ten on the day after a statement, for damage and from a wounding up. Never for a plain blow.
- DS Ellis comes at nine by the real rule: for a wounding or worse once reported, and for the street's talk when it is loud. The prototype's detective then walks the street as before.
- The hours in the cells in the town's answer are the real ones (6 for damage, 8 for a wounding, 12 for a robbery, 22 for a killing). The arrest scene itself still charges the prototype's hours and bill until the police builder switches it over.
- The player notices: the morning after a seen deed is quiet until nine. Then somebody is seen to have gone. The day after that, a constable. He has a day and a night to reach a witness.
- Frightening or paying a witness before nine stops the statement and never the talk.

### 8. Each person's temper

- The real town holds a nerve and a goodwill for each of its 41. The prototype holds a nerve and a liking for each of its 28. The same real rule is asked with either. A timid witness stays at home; a steady one goes; a friend does not.

### 9. The week's own beats

- The real week makes its own stories of his answer to each night's ask, Ada's tea, and Sheila's question. The prototype's story still decides when those scenes play. His answers are told to the town when he gives them (a no, a no-show, the envelope handed over, the tea, the week's answer), so the town's talk of them is the town's.
- The town also says each hour whether, by its own week, Ada asks him in today and whether Ron has the envelope tonight. The story builder may follow those; today they are written in the log only.

### 10. The Ledger

- Unchanged in its rule: only what Tom saw, heard or was told. It fills from the same minds as before, which are now fed by the real town for the nine.
- New for tests and for the claim check: every reaction (a remark to his face, a statement, DS Ellis, a constable) can print the chain of who saw it and who was told.

### 11. Saves

- The save holds the town as one plain object, written by the town code's own save routines, and the crimes still to be reported. Saved and loaded, the town is the same to the last character and plays on the same.
- A save from before today has no town. It opens a fresh one at its clock. What its people saw with their own eyes is told to the new town; what they had only been told is not carried, and the new town's talk starts again from those who saw. The game's log says how many things were told and how many could not be.
- A saved town that cannot be read (a changed cast file) is replaced by a fresh town at the clock, and the log says so. The week itself always loads.

### 12. If the simulation file is missing

- The page fetches one-sim.wasm when it starts. If it is not there or is an older build, the game starts and plays on the prototype's old rules, and the log says: "The town's own rules could not be loaded".

## What is still the prototype's own, and why

- Who can see or hear him at all: the map, the light, the rain, lines of sight, windows. The real game has its own street; this is the prototype's.
- How far a sound carries: the prototype's numbers. They agree with the real rule where it was checked (a footstep at three in the morning carries 3.6 m, at noon nothing).
- Liking, fear, and what each person calls him.
- The talk of the 19 people the real cast lacks.
- Money, debts, jobs, fares, fights and talk: never in the town code. Each is being written as a separate piece with its own test cases (production/lane/ONE-SHOT-PORTING.md).

## For whoever owns the town code (nothing under ue-probe or ledger was touched)

1. Only damage brings a constable in the packaged game. The bridge now follows other crimes on the deed's own timetable and files them in the real police file. Golden rows for a wounding reported and a man taken for it would hold this to the Core.
2. The town says who holds a story, not each telling. One more door for the tellings would bring back "two people stop talking as he passes" for the nine.
3. A witness of the deed can be silenced in the real rules (Silence.h); that is not behind the door, so the bridge keeps its own "will not go" for the crimes it follows.
4. The golden table has no row for an open act or for two deeds. The bridge's handling of both is held by its own checks only (T11, T14).
