# CHECK 2: independent check of the browser build (stories S04, S05, S06)

Checker: a fresh subagent, 20 Nov 2026. Build: /home/claude/w3 (dist/ played, src/ read). No git, no network.
All play was by my own scripts in /home/claude/chk-out/scripts (s04.mjs, s05.mjs, late2.mjs, runs.mjs, s06.mjs,
s06b.mjs), through play.mjs: key presses, mouse look and walking at a player's pace from the saves in
/home/claude/chk-saves. One browser at a time. No page errors and no system faults were reported in any run.
I read game state through P.world only to print what happened (positions, money, the printed chain). I never
wrote to it.

## A. Three stories played

### S04 The outfit's first ask (from "S03 takes", a different branch from the one the story test uses)

What I pressed: I walked to the office door, pressed E to go in and held Z. Ron spoke 0.02 real seconds after
I came in. At 23:03 it was already dark, and Ron was standing on the street by the door (6.2, 38.5). He was
put on the office mat in the same frame Tom came in. So there was no wait, and he did not walk in.
He said the whole ask: the envelope, the ferry landing after ten, the shelter under the last lamp past the
Harbour Office clock, the dark coat on the hook.

Off the path:
- I picked "What is in the envelope?". He answered in character ("You don't ask, boss...") and asked again. Good.
- I typed my own words, "Is it drugs, Ron?". He answered "Thirty years on the dock, I never minded rain. It's
  the standing still." That has nothing to do with the question, and the suggested lines then went empty.
- I picked "I'll take it", then "No. Hold off a minute". He said "Right. It'll keep." and the offer came back.
  Then I took it with Yes. Asking twice before taking holds.
- I pressed T with no coat on: "Nowhere to hide it: the dark coat is not on him." Good. I pressed C with no
  coat: no line at all. At the hook the prompt "T Put the envelope under the coat" was offered while the coat
  was still on the hook.
- I took the coat (E), put it on (C) and pressed T: the envelope went under it. At the same moment a line came
  up saying "Two things under the coat is all it hides", with only one thing under it.
- I put the envelope in the locked drawer (G, "Put away the envelope"). Then I took the crowbar off the nail
  and a cosh from the drawer, so two things were under the coat. Open said "He carries a crowbar and a cosh
  under his coat." The drawer listing tracked every move: "a cosh, the envelope", then the envelope alone.

Verdict: REAL IN PLAY for the ask, the decision, the coat, the two-thing limit and the drawer, all done by keys
and all different off the path. It is thin in two places. Ron's arrival is a teleport onto the mat, not a walk
in from the rank. And typed talk gets an unrelated stock line.

### S05 The carry past the constable (from "S04 yes")

The lit quay (s05.mjs): I left by the front door at 23:46 and walked west along the quay. "Measured footsteps
on the wet. The constable is on his beat." showed at 366.5 s, as Tom came out of the door (the constable was
6.8 m away). The constable then kept within about 1.6 m of Tom for the whole walk: at -20 he was 1.6 m away,
at -35 he was 1.6 m away. He called "You, there. Hold on a minute." at 394.0 s, which is 27.5 real seconds
after the first sign. The challenge offered Stand, Run and A word.

Off the path 1, "A word" with the envelope under the coat: the reply came straight back as "I will keep the
envelope. And your name, sir. I am writing it down." No word was exchanged. The result is exactly the same as
Stand. The envelope was gone, and the Day book had "Searched by the constable on Quay Street. He kept the
envelope" and "The constable has the envelope. The landing is missed tonight". At the landing afterwards there
was no man, no prompt and no "Mickey's?". That part holds.

Off the path 2, never going (late2.mjs): I stood on Quay Street and held Z from 23:46. The constable passed
within 13 to 16 m and did not challenge (no clear sight). At 01:45 the landing shut, and the Day book had "The
landing shut with the envelope still on him. The ask is failed; Ron will hear of it before he does." At about
04:00 the game's "dead on his feet" rule put Tom to bed in the flat. The save holds the flat, but no save note
showed.

Off the path 3, Run (runs.mjs). This is the story's branch 4, played by my own route back east along the quay:
- 395.2 s: Run picked. 396.2 s: "A hand on his shoulder. Nobody runs from me for nothing." The chase record
  says caught after 1 second, and the envelope was taken silently.
- In the next 8 real seconds the constable was at (6.4, -54.9), 98 m from Tom. The arrest code had moved him to
  the top of Quay Street. Tom ran on, free, up Quay Street.
- The constable then walked back for about 60 real seconds. He reached Tom at (7.1, 5.9), and only then did
  the arrest talk open.
- So the story's branch 4 (a chase of up to 90 s, lost after 7 s out of sight, then the constable looking round
  the last spot) did not happen. The constable challenges from arm's length, and from there Run is caught at
  once. The story test's own route reaches "lost" only through its exact timing; my route, with slightly
  different timing to the same spot, was collared.

Verdict: THIN. The beat walk, the footsteps notice, the search keeping exactly the unlawful thing, the late
failure and the Ledger lines are real. But Run, the branch that makes the constable a chase, collapses into
"caught in 1 s" followed by a visible teleport. "A word" is a dead answer when anything is carried. And the
constable walks alongside Tom at 1.6 m for 25 s before speaking.

### S06 It comes back, and the count (from "S05 home quay", the searched branch)

s06.mjs and s06b.mjs. In s06.mjs I went down with the coat still on and walked first the wrong way, to the top
of Quay Street, then back to the pavement. In s06b.mjs I took the coat off and stood on the pavement at
(7.6, 33).

- The road, as watched in s06b.mjs: the outfit's man appeared at 08:04 at (-30, 44), 39 m away and out of
  Tom's sight. He walked to the rank and told Ron at 08:52 (the chain shows "Ron Kirby"), and Ron told Darren
  by 09:02. Tom had sight of the man while he walked (los true at 11 m and 5 m). After that, standing 4.7 m
  from Darren for another game hour brought nothing. Darren speaks only within 4.5 m and while standing still,
  and nothing tells the player to walk up to him.
- In s06.mjs, Darren's first line to Tom was about the coat ("That's Mickey's coat. I'd know it across the
  river, Tommy."). The offer "L The Ledger: what he knows, and how sure" then appeared by 10:07, which only
  happens after Darren has said it to his face.
- Ron, who knew, was put on the "avoided" list (his back turned). Heads together showed in the Ledger:
  "Heads together with the night driver, eyes on Tom. Saw it. A guess."
- The street's lines repeat across people. "They say you're on the cabs yourself. Folk like that." came from
  the night driver, the woman at the fish shop and Ron. "Driving yourself now? Mickey never did, after the
  first year" came from the night driver and Ron. Ron also says "The Ledger [L] holds only what you have seen
  and heard yourself": a key hint in a character's mouth.
- The count, at 10:07 with Sheila at her desk: "The tin has ten pounds in it. The book can hide ten pounds and
  four fifths of the fares really driven since it was last done: about eighteen pounds today." The tool says
  the limit is 1822 pence, which is 1000 + 0.8 x 1028, so it is right. I picked "All of it". The tin was inside
  the limit, so it went through: the tin went from 1000 to 0, the fare book from 0 to 1000, and the pocket from
  3378 to 4378. The flows balance (pocket 4378 = 4378 by flows, tin 0 = 0, holds true). E again: the count
  prompt was gone and only "Talk to Sheila Dunn" was offered. The "over the limit" talk could not be reached
  from this save because the tin is under the limit.
- Escape, Save, Quit, Continue: before was game minute 2047 at (1002.2, 998.8) in the office with 40 Ledger
  notes and the same money. After was minute 2048, the same place, the same 40 notes, the same money.

Verdict: REAL IN PLAY. The news really travels by people walking and meeting, and the count really moves money
under its rule. Thin edges: the courier is placed by assignment out of sight. The road is one fixed route
(courier to Ron at the rank, Ron to Darren on the pavement), not general gossip. And the street's lines are
shared between people.

## B. Five parts of the code

### src/game/back.js: THIN
The knowledge is real data: a thing is known by who saw it and passes only when two people stand within
2.2 m. But the passing is one hard-coded choreography, not a gossip system:
- "the outfit's man goes to Ron at the rank in the morning, Ron walks over to Darren on the pavement" (the
  header comment). road() names exactly courier(), P_('ron') and P_('darren').
- Ron and Darren are pinned to their spots: `keep(R, 'rank')`, `keep(D, 'pave')`, and "Darren keeps to the
  pavement until he has said it".
- The courier is teleported in: `Object.assign(M, { ... space: 'street', x: from[0], z: from[1] ... })`. It is
  only done where Tom cannot see (`!G.env.los(...) || hyp(...) > 60`), which is honest staging, but staging.
- Darren's line is picked from a fixed table by what he knows (darrenLine). This is correct by the rules: he
  never mentions a run nobody told him of.

### src/game/carry.js: THIN
- The landing man is put in place by assignment when the landing opens:
  `Object.assign(M, { override: null, hold: true, ... x: mx, z: mz ... })`.
- Any loss of the envelope counts as the police:
  `if (!holdsEnvelope() && !(G.x.crime.stored || []).some((s) => s.id === 'envelope')) return lost(x, 'police');`
  That holds today only because the constable's search is the only way to lose it.
- Real: the hand-over pays through `earn(T.firstCutPence, true, ...)`. Who saw the cab is worked out by
  distance and line of sight (`hyp(P.x, P.z, c.x, c.z) < ... && G.env.los(...)`). The lateness rule is a real
  window (`Math.max(night0 + 1440 + T.landingShutsHour * 60, o.takenT + T.windowAtLeastGameMinutes)`).

### src/game/count.js: REAL IN PLAY
- The limit comes from the economy (`cap = washRoom()`). An over-wash asks first ("That's more than the book
  will stand, love. You sure?"), and if done anyway it costs Sheila's regard and counts `m.booksOff += over`.
- Every penny goes through `flow('tin', 'pocket', amt, ...)`, and in play the balances held.
- Once a day: `if (X('count').day === dayNow() ...) return`. I saw the prompt go after one count.
- One special gate to note: the count is offered only if `G.story.flags.tour` (Sheila's walk-round) is done.

### src/game/law.js: REAL IN PLAY for the beat, with a broken branch
- The beat really walks between two ends: `goToPoint(P, nx[0], nx[1], T.beatWalkMetresPerSecond)`.
- He challenges only on seeing Tom: `const s = sense(P, tomTarget()); if (!s.see || d > T.challengeWithinMetres) return;`.
- His footsteps go into the mix at their distance:
  `G.hooks.heard('steps', Math.max(0.05, 0.6 * (1 - d / T.beatHeardWithinMetres)), 'the constable')`.
- Fault: in carChaseStep the line `if (los || c.lx === undefined) (c.lx = t.x), (c.lz = t.z);` uses `t`, which
  is not defined in that function (only `tx, tz` and `x` are). The first frame of any patrol-car chase ("Put
  his foot down") throws a ReferenceError, so the car chase can never end. Found by reading; not played.
- The cause rule counts a hidden envelope: `carryingAtNight: !!t.carry || items.some((i) => i.unlawful) ...`.
  So the constable "suspects" what is out of sight under a coat.
- After "caught" it hands off to `G.story.arrest`, and police.js then does `P.x = POL.arrivesAtXMetres;
  P.z = POL.arrivesAtZMetres;` (-86 on Quay Street). That is the visible teleport seen in play.

### src/game/outfit.js: THIN
- Ron's arrival is an assignment, not a walk: `R.space = 'mickeys'; [R.x, R.z] = roomPos('mickeys', ROOMS.mickeys.mat[0], ...)`,
  with a door sound.
- After the ask he is put back on the street: `R.space = 'street'; R.x = ROOMS.mickeys.street[0] - 0.8; ...`.
- The decision, the twice-asked no, the drawer and the coat are real and keyed. Staying away is a real timer
  (`ronWaitsForAnAnswerGameMinutes`) that ends with the envelope stored in the drawer.

## C. Faults met, most serious first

1. Run from the constable is caught in 1 second, then the constable teleports about 100 m away and walks back
   for about a minute while Tom runs free, after "A hand on his shoulder". Steps: Continue from "S04 yes". Walk
   to the office door, E Leave. Walk west along the quay (6.4,42.8), (-20,43.2), (-44,43.2) until he calls out.
   Pick 2 (Run) and run east to (0,43), then (7,40), then up Quay Street. You get "A hand on his shoulder" at
   +1 s, yet the constable stands at (6.4,-55) 8 s later. The arrest talk opens about 60 s later at the top of
   Quay Street. Story S05 branch 4 is not met on this route.
2. Patrol-car chase code throws: law.js carChaseStep uses an undefined `t` (`c.lx = t.x`). Steps (by
   reading): drive recklessly in the patrol car's sight and pick "Put his foot down". The step throws every
   frame and the car chase never ends.
3. The constable walks beside Tom at about 1.6 m for about 25 real seconds before he calls out. Every
   challenge therefore comes at arm's length, which makes fault 1 near certain. Same steps as 1: see the
   distance column in s05.mjs output (1.6 m at x = -20 and at x = -35).
4. "A word" is a dead answer when anything unlawful is carried. There is no exchange; it is identical to Stand
   ("I will keep the envelope"). Same steps as 1, pick 3.
5. Typed talk gets an unrelated stock line, and the suggestions vanish. Steps: Continue from "S03 takes",
   go into the office, let Ron ask, Tab, type "Is it drugs, Ron?", Enter. He says "Thirty years on the dock, I
   never minded rain. It's the standing still."
6. Ron teleports onto the office mat the frame Tom enters, with no walk in and no wait. Steps: Continue from
   "S03 takes", E at Mickey's door. Ron is talking within 0.02 s, though he was on the street at (6.2,38.5).
7. The Day book's week summary lowercases a name: "Mon 15 Oct: Laid hands on darren Milner. Collected from
   darren Milner." Steps: Continue from "S04 yes", L, turn to Day book.
8. The People index lists "Darren Milner" twice. Steps: Continue from "S05 home quay", go out, L, People.
9. The same street line comes from different people: "They say you're on the cabs yourself. Folk like that."
   (night driver, fish shop woman, Ron) and "Driving yourself now? Mickey never did, after the first year"
   (night driver, Ron). Steps: Continue from "S05 home quay", go out, stand at (7.6,33) from 07:20 to 08:30.
10. Ron says a key hint in his own line: "The Ledger [L] holds only what you have seen and heard yourself."
    Same steps as 9.
11. Wrong or missing small prompts in the office: "T Put the envelope under the coat" is offered at the hook
    before the coat is on; C with no coat gives no line; "Two things under the coat is all it hides" shows when
    one thing is under it. Steps: from "S03 takes", say yes to Ron, walk to the hook, look at the prompts,
    press C, then take the coat, C, T.
12. Darren says it only within 4.5 m and while standing still, with nothing to draw the player in. Standing
    4.7 m from him for a game hour after he knows brings nothing. Steps: as 9, with the coat off; stand at
    (7.6,33) until 10:00.
13. Place mislabel: the Day book says "Searched by the constable on Quay Street" for a search at x = -36 on
    the quay. Steps: as 1, pick 1 or 3, then L, Day book.
14. The collapse ("dead on his feet", about 04:00) saves the game but shows no save note. Steps: Continue from
    "S04 yes", go out, stand at (7.3,22) and hold Z for about 20 real seconds.

Not checked: S05 by the yard and the cab, S06 from the other three saves, the "over the limit" count (the tin
in "S05 home quay" is under the limit), and the car chase in play.
