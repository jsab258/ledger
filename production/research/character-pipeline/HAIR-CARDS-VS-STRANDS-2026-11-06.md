# Hair cards against strands, 6 November 2026 (item n02-9)

Status: run in part, in the packaged game (build 2af162e), 20:22 to 21:01 Swiss. Nothing from it is kept in the game. Pictures and frames: F:/LedgerTools/gate/new/hair-cards-vs-strands-2026-11-06/ (106 MB). One fresh small reviewer (review.json in that folder): the bald faces, the recolour, Tom's hair and all 24 table figures hold; the corrections are in the text below. The first launch's refusal did not repeat: the same game started normally.

## What was found

1. **Epic's switch leaves everyone bald.** With r.HairStrands.UseCardsInsteadOfStrands 1 Ron and Sam have no hair, moustache or beard, and Lena only a pale cap. The engine says why: "If no cards data is available, nothing will be displayed" (GroomManager.cpp line 50, 5.8.2). Our people's face level 0 maps to groom level 1, which holds strands; Epic's High build keeps cards only at level 3 (MOUSTACHE-LOD-2026-11-02.md). So the switch is not usable on these people as they are built.
2. **The real cards show one detail level down, in a different colour.** r.SkeletalMeshLODBias 1 reaches them, hair and moustache whole. Side by side at the same moment of the talk: Ron's dark hair turns grey, Sam's dark hair turns light brown, Lena's dark hair turns grey; Ron's moustache and Lena's brows lighten too. His ruling of 3 November says no colour change where detail levels switch, so this is a fault in any character reaching that level, seen for the first time here. Cause not read; the hair recolour reaching strands and not cards is the likely place (unverified).
3. **Whether it already shows in ordinary play is not shown.** At the game's start, by Tom's camera with nothing forced, a fair-haired figure in white stands a few metres ahead. The session read it as Sam, dark in his close-up; the reviewer finds it side-on and tiny, and fair in both Tom's-camera pictures, so not shown to be him.
4. **Tom does not.** His hair reads the same dark brown at his normal level and one level down, by day, in one picture each, a tiny back view (tom-camera-strands-day.jpg, tom-camera-level1-day.jpg; they also differ in a pedestrian's pose and in darker roofs in the first, so they are not a controlled pair). The moustache note says Tom's build sets groom parameters and Ron's does not, which fits, though the cause is unread. So by day, cards are not the likely source of his pale crown; the night and the office, where that fault was seen, were not tested. No try spent on the crown.

## Views

| View | Strands | Forced cards | Level 1 (real cards) |
|---|---|---|---|
| Street, five cameras, day | taken | taken: faces too far to tell | not taken |
| Street, five cameras, night | taken | taken: faces too far to tell | not taken |
| Talk close-up, day (Ron, Sam, Lena) | taken | bald | taken: colour changes |
| Talk close-up, night | not reached: no switch films a talk at night | same | same |
| Tom's camera, day | taken | not taken: nobody near enough is worth a third run | taken: Tom unchanged |
| Tom's camera, night | not reached: the page pictures hide Tom | same | same |

The page pictures also leave out the three undressed talkers, so the street frames hold only distant people. The tester refused once at 20:56, input 32 s old, and started at 20:59; the second start used --force, its own keys reading as the PC in use. -FaceAB's films need -PreparedAck, or the thinking sounds do not play and no frame is written; both of the first talk runs wrote nothing for that reason.

## Frame cost, corner's crowd (hook camera, 1,200 frames, no voice beside, picture level High; runs.jsonl)

| Case | Frame median ms, day / night | Slowest 1%, day / night | Card time median ms, day / night | Card memory MB, day / night |
|---|---|---|---|---|
| Strands | 15.17 / 15.12 | 20.02 / 21.51 | 13.78 / 13.90 | 5,615 / 5,607 |
| Forced cards (bald close to) | 15.13 / 15.13 | 20.91 / 20.73 | 13.75 / 13.89 | 5,583 / 5,572 |
| Level 1 | 15.12 / 15.17 | 20.70 / 20.52 | 13.78 / 13.91 | 5,584 / 5,566 |

No difference above noise in time; about 30 MB less card memory, from one run each. **This does not show hair costs nothing.** Card time sits at about 13.8 against a 14.0 ms line in every case, which suggests the game's own drawing size is absorbing any change (unverified), the hook camera has few people near, and draw calls are equal in the strands and cards rows. Only the corner's crowd at this distance is answered.

## Frame cost, one person close

Unread: no switch measures a talk's frame cost. -FaceAB starts no profile, and adding one needs a game change, not made for a comparison on the waiting list.

## What could not be done and why

Night talk and Tom's camera at night: no switch reaches them. One-person cost: above.
