# What could not be done, and why

18 November 2026. Most important first.

## 1. The measures file was played by a script, not by a person

`measures.json` comes from one full week, Monday to Friday, played through the test hook by
`test/week.mjs`. It proves that every measure counts and that the export works. It says nothing about how a
player behaves: the opens per hour, the seconds per visit and the find-the-fact times are a script's. The
pad half of find-the-fact is empty, because the script used the keyboard road. Real numbers need a person;
the screen, the export and `LEDGER.measures()` are ready for that.

## 2. The Tuesday night pause was not reproduced

The cause is still not proven. The new check (`LEDGER.check.nights()`) steps through Tuesday and
Wednesday nights and finds every pause paired with its resume. What I changed is the likely cause: fades
and goodbyes waited on the browser's timers, and a browser holds those back, by up to a minute, in a tab
that is not showing. They now run on the game's own steps. If it happens again, `LEDGER.pauses()` and
`LEDGER.pauseFaults()` will say which pause, when, and why.

## 3. Not every named person who sets off gets there

Fault b is fixed: nobody stands still any more, and Ron walks home. But the new arrivals check found a
second thing, which I did not change:

- With Tom away, in 26 game hours, 157 walks set off, 139 arrived and 14 were given up for the next place
  in the routine before arriving. 8 of the 14 are walks to or from the map's edge by the two drivers and
  the watchman (about 250 metres against one-hour slots). The rest are routine hours shorter than the walk
  (Lee, Nora Cronin, Dennis, Albert).
- Near Tom, people walk at their real pace (out of his sight they move 3.2 times faster). So Norman Dent's
  night rounds to the warehouse row (86 and 114 metres in 60 game minutes) are never finished while Tom is
  near.

Why left alone: the fix is to retime routines or change walking pace. Either changes how long people spend
together, and so the gossip numbers. The brief says to change nothing else. It needs a decision.

## 4. Not every number is in `LEDGER.rules`

In the table: time, seeing, noise, memory, gossip, naming, police, money, prices, jobs, fares, light,
weather, rest, the Ledger, watching, noticing, walking pace. Still in their own files:

- the confrontation ladder in `fight.js` (about 170 numbers in its tables);
- the weekly schedules in `cast.js` and the inner numbers of `routines.js`;
- some coefficients inside `scenes.js` and `talk.js` (how much a line moves regard or fear).

Why: moving them is safe only one at a time with a check after each, and there was not room for all of
them in this round. Nothing reads a rule from two places.

## 5. The Ledger screen test: three limits

- A typed letter cannot jump to names under E, L or Q, because E and Q change part and L closes.
- In a talk, L opens the Ledger only when the typing box does not have the keys (after Tab). Otherwise L is
  a letter in Tom's sentence. Esc and L both close it and give the talk back.
- A pad drives the Ledger only. The rest of the game still needs keyboard and mouse, or touch.

## 6. One entry can still disappear

An entry that says nobody saw an act is withdrawn if a watcher is written down within two game minutes of
it (about seven real seconds), as one piece of writing. After that it is struck through with the day and
the reason. The brief says never deleted; this is the one exception, made on purpose and listed in the
design notes so it can be judged.

## 7. No zip beside the page

The host refuses a page that carries an archive. So the source is published as separate files under
`source/`, the game's "Source and files" screen can save them as one zip where the host allows saving, and
the same zip was sent in the chat.

## 8. Two earlier test scripts are not in the published set

`test/play.mjs` and `test/logic.mjs` are the first round's scripted run-throughs. They still run without an
error on this build, but they print a log to read, not a pass or fail, and some of their steps are out of
date since the talk changed (they press keys for choices that are now lines in a talk). Bringing them up to
date is a job of its own, so they are left out. The published tests are the ones that pass or fail.

## 9. Not checked by me

- A real AI follow-up line in talk: the test sandbox has no live voices, and in the published page the
  first call asks for a permission that is the owner's to give.
- The build on a second machine: same checksum twice on one machine, not tried on another.
- The published page in the owner's own browser, unless the report in the chat says otherwise.
