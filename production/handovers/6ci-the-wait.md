# A way to wait, and the clock

Town list 6ci and the clock. Decided by the town, 29 September. Design:
game-design/waiting-2026-09-29.md. Research: production/research/waiting/NOTE-2026-09-29.md.
Code: ledger/Assets/Scripts/Core/Waiting.cs.

**What the player gets:**
- The day runs at two game minutes a real second, twelve real minutes a day.
- He can wait, or sleep, until a chosen time, or until the next thing the town
  has for him.
- A wait ends early, with one plain line, for: Ron with the envelope, the
  landing, Ada's pot at nine, a constable, DS Ellis, Sheila's Sunday and her
  answer, and his release from the cells.
- Each line is shown once. A sleep is a wait, and Ron knocks.

## Wire it

1. **Before offering a wait:** if `Waiting.Refused(beats)` gives a line (during
   Sheila's walk-round), show it and offer no wait.
2. **Run a wait an hour at a time.** Before each hour, call
   `Waiting.Next(now, until, beats)`. `beats` is a `WaitBeats` holding:
   - the arrangement, Ada's tea, the police file with the mill and the inquiry,
     the week's end, and any custody;
   - `AtAdas`, true while he waits in Ada's house;
   - his walk in game minutes to Ada's (`TeaLead`), the landing
     (`LandingLead`) and the office (`OfficeLead`);
   - `Shown`, the lines already shown.
3. **When it gives a stop:** end the wait at `stop.At` and show `stop.Line` as
   plain text. Then call `Waiting.Showed(beats, stop)`. A stop at `now` is a
   line due at once: Ron at the door, or a walk whose time has come. For Ron,
   `Delivered(stop.ForDay, …)` uses the night's day even after midnight.
4. **Offer "wait until…"** each stop of `Waiting.Ahead(now, until, beats)`,
   such as "until Ada's tea".

## Port

`Waiting` and `WaitBeats`, and `PoliceFile.ConstableWouldCome` and
`EllisWouldComeAll` (`ConstableComes` and `EllisComes` now call them). Match
the rows behind `--awaiting-port`: `Wait`.

## Save

`beats.Shown`, a list of strings, kept with the game's save.

## Walk it

1. On night one, wait from six until morning. The wait stops at eight: "Ron's
   at the door with something for you."
2. Take the envelope and wait again: it stops before ten for the landing.
3. On day 3, having been asked in, wait from six: it stops for Ada's pot.
4. Wait again after any stop: the same line never comes twice.
