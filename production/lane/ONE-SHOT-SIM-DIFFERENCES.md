# The real town inside the prototype: what changed for the player

The one-shot's second run, 20 November 2026. Way A, his decision: the game's own C++ town code, compiled for the browser, now runs inside the prototype's page. This file says every place the prototype's old copy of the town's rules differed, what was switched to the real rules, what was not, and what the player will notice. The measurements behind it are tools/lane/one-sim/DIFFERENCES.md (19 November); nothing under tools/lane/one-sim/ was changed.

## In short

- The real town code travels inside the game's one script (about 420 KB, compressed about 110 KB). The page loads nothing extra and falls back to nothing: without the town code the build stops and says so.
- Every simulation step hands it the clock. Each sighting by a person of both casts is told to it. A thing damaged is the week's deed, with everyone who saw it. Each hour's doings come back and drive the game.
- The town is in the save. A save from before today still loads: it opens a fresh town at its clock and tells it what its people saw with their own eyes.
- Not everything could be switched, and this file says so plainly below. The two largest things left are names (a canon question) and violence reaching the police (a call the town code's front door does not have yet).

## What now runs on the real rules

| Thing | Before | Now | What the player notices |
|---|---|---|---|
| Talk between the nine people of both casts (Sheila, Ron, Darren, Alison, Father Walsh, Ada, June, Rita, Hal) | gossip.js passed one story a telling, by chance, every 4 game minutes, to anybody within 4.8 m | The real town's talk passes it, every 6 game minutes, only between people its cast file ties together and puts in the same place that hour. gossip.js no longer passes anything between two of these nine. What the real talk passed to them becomes their memory in the prototype, with who told them and how many tellings from the one who saw. | A deed reaches about as many of them on its first day, then stops sooner: about five of the nine hold it, where eight did. It does not cool in a day. The same week plays the same way twice: the real rules use no chance. |
| Damage (a window put in, a door forced, a car taken) | The prototype had no act that damaged a thing | These are the deed the real week follows. Whoever is there and did not see it done finds it; others find it as their routine brings them past (A38); who saw it done goes to the police at nine next morning unless on his side or of the trades that never go. | Damage brings the law the real way: a statement at nine, DS Ellis a morning later, a constable at ten the morning after that. |
| DS Ellis's mornings | Thursday or Friday, when his name was "loud" by the prototype's own number | She comes on the mornings the real rules send her (from the second day, for talk, or for a deed) | She can come on any morning from Tuesday. |
| The arrest for damage | The prototype's own statement rule and a next-day visit | The real town says when he is taken for the deed; the prototype plays the scene (a constable walks to him; go, or run) | A day slower than before, as the real rules are. |
| Who finds an unseen deed | Nobody | The real town's routines | Somebody comes by and finds it. |
| The week's length | Five days, ending Friday afternoon | Seven. Sheila asks on Sunday, as the design (section 16) and the real rules have it. Rent is still due on Friday. | Two more days in week one. |
| His answers | Kept in the prototype's own flags only | His answers to the nights' asks and to Sheila are also told to the real town, so its own stories of them are true | The outfit's man holds the right thing about him. |
| Saves | The prototype's own minds and events | The same, plus the town as the game's own save writes it (about 17,000 characters) | Nothing: a save loads and the town plays on exactly. |

## What is still the prototype's own, and why

| Thing | Why it was not switched | What it means |
|---|---|---|
| The other 19 named people (Pauline, Kevin, Terry, Wayne, Brenda, Lee, Grace and the rest) | They are not in the real cast file, whose other 32 people have no names yet. Which names stand is a canon question (DIFFERENCES.md, decision 1), never the bridge's. | Talk that involves any of the 19 still passes by the prototype's own rule. A story therefore travels through two rule sets, joined at the nine. |
| Where people stand, hour by hour | The real cast file has 30 places; a table from those to the prototype's map is not built, and some real places have no spot on the prototype's map. | People keep the prototype's routines. The real town believes the nine are where its own routine puts them, so who it lets talk to whom can differ from who is seen standing together. This is the largest disagreement left. |
| How well a witness sees him | The real rule has no call on the town code's front door yet. The prototype's own geometry and light decide, and its memory of a sighting is read as a rung (recognised, a face, a mark, a silhouette). | Who can name him, and from how far, is still the prototype's. The new hiding rules (A1) are added on top of it. |
| Violence and the police | Through the front door only the damage deed is reported (decision 5). | A blow, a weapon or a killing seen by one of the nine is told to the real town as talk, and can bring DS Ellis. Statements about violence are still made by the prototype's own rule. Until the front door has the call, two rule sets decide who goes to the police. |
| Decent and open acts (a fare, a debt struck out, the rent paid) | The front door has no call for a story that is not about his hidden life (decision 7). | Good deeds travel only by the prototype's own talk, so they do not reach the nine through the real town. |
| What each person thinks of him and what they call him | The real counterparts are not behind the door (decision 2, recommended answer). | Liking, fear and names stay the prototype's, fed by memories that now come partly from the real town. |
| The asks' and the tea's hours | The story's scenes are written round the prototype's own hours. | Ron comes when the prototype's story sends him, not at eight as the real rules do; Ada's tea is at the prototype's hour. His answers reach the real town either way. |
| Passers-by | The real town's talk is between its 41 people only. | A passer-by who saw damage is not told to the town. He still carries what he saw to the first named person he stands near, by the prototype's rule. |

## Decisions taken here, within his rulings and the recommended answers

1. The week is seven days (decision 3). The design already says Sunday, and the real rules refuse Sheila's question before it.
2. Damage is in the game (decision 6), as the addendum's A35 designs it, and is the deed the real week follows. The real rules follow one deed a week: a second piece of damage in the same week is told as talk, one telling a witness, and is not found by passers-by.
3. Violence stays with the prototype's own statements for now (decision 5, the recommended "accept it for the first swap"), said here and in the known issues.
4. Licences: the town code brings pieces of the LLVM C++ library, its helper routines and wasi-libc into the page. Both lines are on the allowlist with his yes of 19 November ("notices kept"). The notices that could be read are in production/licences/one-sim/; the page's files name them. Four notice files were still unread on 19 November and are still to add before a wide release; this is recorded, not asked.

## Old saves

A save from before today has no town in it. It still loads. A fresh town opens at its clock and is told each thing one of the nine saw him do with their own eyes. Lost: what people had only been told (the real talk starts again from those who saw), what the 19 saw, decent acts, and the real week's beats already past. The prototype's own minds are kept as they were, so what people think of him is unchanged at the moment of loading.

## How it is tested

- test/game/town.mjs, in the page: the town opens; its clock is the game's; a blow seen by Darren is told to it and passed on; a window put in is the deed, Ada its witness, and she goes to the police at nine; a save loads and plays on with the deed still held; a telling prints its chain back to the one who saw (ER-EYES-05).
- tools/lane/one-sim's own checks (one-sim.sh all) hold the town code to the C# Core, as before.
- Not yet: a whole played week compared on both sides, and the older week tests re-recorded against the new town (their records were made with the old one).
