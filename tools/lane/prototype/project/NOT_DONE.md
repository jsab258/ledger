# What could not be done, and why

18 November 2026, second round. Most important first.

## Lane round 1 (18 Nov, the eight fixes): what is still open

- A person closes a talk in their own voice when their written lines run out, but the talk stays open with only
  Leave offered; typing your own words still gets the closing line again. Live talk (inside claude.ai) is not
  limited this way and was not tested here.
- Bubbles are hidden behind walls only on the street (rooms have no line-of-sight test), and "on screen" means
  within 20 m and in sight, not checked against the camera's frame.
- Only Ada's window prompt was found naming someone too early; other prompts were not searched one by one.
- Only Ada's tea note was found outliving its hour; the Friday rent note and the scrapyard's seven o'clock were
  not checked the same way.

## 1. Every walk arrives in the two cases asked for, not wherever Tom stands

Both arrivals checks pass: Tom away, and Tom kept at the rank for the whole 26 hours. But the rule that
makes this hard is still there, as asked: within 90 metres of Tom people walk at their real pace, a game
minute to the metre. If Tom stands somewhere else, on Copper Row or by the scrapyard, the walks near him
there are the slow ones, and a long walk through his sight can still outlast its row and be given up.
`tools/walk_times.mjs` checks the rank and nowhere else. To hold wherever Tom stands, either every row needs
room for its whole walk at real pace (Albert's day would not hold two stops), or a person finishes the walk
they have started before turning for the next place. The second is a change to the routines' logic, not to
pace or seeing, and was not asked for. It needs a decision.

## 2. The retiming went much further than the map's edge and the watchman

That is what the check with Tom at the rank required, but it is more change than the brief names: 22 people
have longer rows, lunch at the caff can take Lee or Dennis four hours when Tom is watching, and some
stops went (Albert's breakfast at the caff, June's Monday evening walk, one of Kevin's runs, one of Terry's,
two of the watchman's rounds). The gossip table in the changelog shows the cost and the gain. If it is too much,
the schedules are now plain rows in `rules.js` under `schedules`, and `npm run walks` says at once whether a
change still fits.

## 3. The numbers 0, 1 and 2 were not examined

Every other number in the 22 rule files is either in `rules.js` or counted with its reason for staying.
But 1,053 zeros, ones and twos were left where they are without being looked at one by one. Most mean none,
all, both, half, a flag or the first of a list; a handful are small rule values (one metre, two seconds).
Not in the table at all, because they are not rules: the map's coordinates (`map.js`), how the Ledger and
the picture are drawn, the camera, the sound.

## 4. The same-week proof covers what a scripted week does

The seeded week gives the same save before and after the numbers were moved, part for part. That week walks,
talks, carries, drives a fare, pays, sleeps and is seen. It does not come to blows or crash the cab. Those
numbers were moved by copying their own text, which cannot change a value, and the town test exercises the
ladder and a fight on the new build; but they are not part of the part-for-part proof.

## 5. The gossip table is one week each

Before and after are the same scripted week with the same seed, once each. It shows the direction (more
meetings, more stories passed on), not an average over many weeks.

## 6. The measures file was played by a script, not by a person

As before: it shows that every measure counts and exports. The pad half of find-the-fact is empty.

## 7. Still open from the round before

- The Tuesday night pause is still not reproduced. The nights check passes again.
- A pad drives the Ledger only. The `/` jump is a keyboard key; with a pad or a finger the A to Z index is
  there to press.
- No zip beside the page: the host refuses archives. The source is published file by file, the game's
  "Source and files" screen can save it as one zip where the host allows, and the zip is in the chat.

## 8. Not checked by me

- A real AI follow-up line in talk: the test sandbox has no live voices.
- The build on a second machine: a clean unpack, `npm ci` and `npm run build` on this one gave the published
  files byte for byte.
- A person playing a retimed week from start to finish: the scripted week, the town test and the checks ran;
  nobody has yet watched Wednesday from the caff with the new hours.
