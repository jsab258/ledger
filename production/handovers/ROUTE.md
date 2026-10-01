# The continuous route: the town's pieces, their inputs, outputs and acceptance cases

For the builder's first goal after the audit of 30 September: wire the clock,
the action, gossip, consequence and reload into one continuous route. This page
covers every town piece that route needs: what the game calls, when, with what
inputs, what comes back, and how to tell it works. The reference is the Core's
own week, played hour by hour by `TownReach --week-waits`
(ledger/TownReach/Program.cs, WeekRows). The route in Unreal should do what that
loop does, in the same order, and reproduce its rows.

## What the route has today (read from the code, 30 September)

- **No running clock.** `GNow` is set by hand to day 1, 12:00, then day 4,
  18:00 and 18:30. A 40-second wall timer stands in for the clock and for the
  wait.
- **Ported and never called:** Arrangement, Waiting, PoliceFile and Custody,
  WeeksEnd, AdasTea, TownNews and Aftermath, TownSave.
- **Ids.** The mill is keyed w1, n2, r3, but the Core looks people up as
  "lena", "sam" and "rocco", so those lookups find nobody.
- **Tick order.** Round 3 ticks at day 4, 18:00, before the hours from day 1,
  13:00 are caught up.

## 0. Ids first

**Key the mill by the cast's own ids** (production/specs/hook-cast.json:
lena, sam, rocco, ada, june and the rest), with every person in the cast in
the mill.
- Acceptance: `mill.Get("rocco")`, `mill.Get("lena")` and `mill.Get("ada")`
  are not null after a new game and after a load.

## 1. The clock and the hour

**A running GameTime**, advanced by the game's own clock (FixedClock), never
by a wall timer.

At each game hour `h` of day `d`, in this order, as WeekRows does. Each call's
inputs are shown:
1. **06:00:** `arrangement.PassedTo(d, mill, now)`.
2. **When the deed happens:**
   - `damage = new Aftermath(place, thing, said, now, Aftermath.DefaultMend(now))`;
   - `mill.Witness(seer, new Fact("player", "window_d" + d, place), said, true, now, certainty, rung)`
     for each witness, with the rung Perception gave.
3. **Every hour after it:** `damage.Tick(mill, cast, now)`.
4. **09:00, from `Aftermath.FirstReportMorning(deedTime)`** (the morning after
   the deed's night: a deed before six belongs to the night before, so one at
   half twelve is reported that same morning; the independent review, B5): if
   `PoliceFile.WouldReport(mill.Get(seer), offence, false, topic, cast.NeverToPolice(seer))`,
   then `police.Report(seer, topic, offence, rung, d)`, once.
5. **09:00:** `why = police.EllisComes(mill, d)`; on "talk",
   `police.HearTheStreet(mill, d, grading, cast, now)`; if not null,
   `PoliceFile.Asked(mill, PoliceFile.WhoSheAsks(mill, cast, now), why, now)`:
   with the cast and the time, she asks only the people on the street then.
6. **10:00, if not in the cells:** `t = police.ConstableComes(d, now)`. **Pass
   the time:** with it, no call is made while he is held, nor for any day but
   today's. If `t` is not null,
   `custody = police.TakeIn(t, now, ownsUp, inTheCoat)`, then
   `Custody.SeenTaken(mill, cast, area, now)`.
7. **10:00 on the tea's day:** `tea.SheSeesHim(now)` returns her invitation
   line, once.
8. **20:00, when `arrangement.AsksOn(d)`:**
   `arrangement.Delivered(d, mill.Get("rocco"), now)`.
9. **Each minute he is in Ada's house, 21:00 to 23:00 on the tea's day:**
   `tea.WithHer(minute)`.
10. **Going down to the landing on an ask night:**
    `tea.WentToTheLanding(mill, now, forTheAsk: true)`.
11. **The envelope handed over at the landing (22:00 to 01:00):**
    `arrangement.Answer(d, NightAnswer.Did, mill, now)`.
12. **His no to Ron** (the talk reply's `refusedAsk`, or a plain no):
    `arrangement.Answer(d, NightAnswer.Refused, mill, now)`. The man at the
    landing knows it only once Ron has been down: read
    `arrangement.NoWordAt`, as for `WoundWordAt`.
13. **23:00 on the tea's day:** `tea.Close(mill.Get("ada"), now)`.
14. **Sunday (the week's day), at the office:**
    - `week.Ask(now, realBook)` when she puts the question;
    - `week.Give(answer, now, mill, cast, arrangement)` on the talk reply's
      `weekAnswer`.
15. **Every hour:**
    - `week.Close(now, mill, cast)`;
    - `TownRounds.Hour(mill, cast, now)` (the rounds every six minutes, and
      the hourly ageing).

    **Catch up every hour in order**, before anything is filed at a later time.

**The wait:** `Waiting.Next(from, until, beats)` gives each stop in turn. The
game stops the skip there, shows the line, and calls `Waiting.Showed(beats, stop)`.

## 2. The talk program, both ways (production/specs/talk-protocol.md)

**Send**, besides what it sends today:
- `ask: {"tonight": arrangement.AskStands(now)}` to Ron;
- `week` (the question standing, and its answer);
- `acquaintance.trusts` and `acquaintance.calls`.

**Act on:**
- `refusedAsk`, with step 12;
- `weekAnswer`, with step 14;
- `threatened`, with `Silence.FileThreat(mill, who, topic, now)`: the one
  threatened holds it first-hand;
- `gaveName`, with `PlayerIdentity.NameTold(mill, who, now)`, as today;
- `ownedUp` and `keepsQuiet`, as today.

With `--early --pending`, a `pending` sentence is made ready and played only
when the same turn's `first` arrives with the same words.

## 3. Save and reload

**One TownSave** beside the mill's agents:
- `TownSave.ToJson()` holds the hints, the ask (with a no waiting for Ron,
  "noTell"), the tea, the police file, the week, the heard ledger and the
  news filed.
- `TownSave.FromJson` restores what play could make and refuses the rest.

Save it with everything else, at the same moments.

**Acceptance: a save and load at any hour of the week, then the rest played
the same way, gives the same row below as playing straight through.**

## 4. Acceptance cases: the Core's week, sixteen ways

Played hour by hour from day 0, 09:00 to day 7, noon, with walks of 30, 120 and
30 game minutes to Ada's, the landing and the office. Three choices vary:
- he takes the envelope every night, or tells Ron no;
- he sits with Ada, or stands her up;
- the window is seen by Sheila, by Darren, by nobody, or there is no window.

Each row is what the Core gives (`TownReach --week-waits`, 1 October, on the
Core with Jafar's two police rulings of that day: a witness who saw the window
reports it the next morning unless on his side, so Darren, who saw it, has him
taken in on day 4; Sheila, one of Mickey's own, never goes to the police about
him and keeps what she saw to herself, so her rows run as if nobody had seen
it; Ada's tea on day 3 comes after any report. Darren replaced Ada as the
second witness, the review of 1 October's M4: behind her window she could never
see Rita's glass in play). The route played the same way must give the same.

| the envelope | Ada's tea | window seen by | DS Ellis first | taken in | Sheila trusts him | day 7 | the arrangement | his answer held by Monday noon |
|---|---|---|---|---|---|---|---|---|
| takes it | sits | Sheila | day 5, for talk | no | never | the day-book | stands (4 nights) | 7 of 41 |
| takes it | sits | Darren | day 4, for talk | day 4, Charged | day 4 | the real book | stands (4 nights) | 7 of 41 |
| takes it | sits | nobody | day 5, for talk | no | day 3 | the real book | stands (4 nights) | 7 of 41 |
| takes it | sits | no window | day 5, for talk | no | day 3 | the real book | stands (4 nights) | 7 of 41 |
| takes it | stands her up | Sheila | day 5, for talk | no | never | the day-book | stands (4 nights) | 7 of 41 |
| takes it | stands her up | Darren | day 4, for talk | day 4, Charged | day 4 | the real book | stands (4 nights) | 7 of 41 |
| takes it | stands her up | nobody | day 5, for talk | no | day 3 | the real book | stands (4 nights) | 7 of 41 |
| takes it | stands her up | no window | day 5, for talk | no | day 3 | the real book | stands (4 nights) | 7 of 41 |
| tells Ron no | sits | Sheila | never | no | never | the day-book | ended (refused) | 7 of 41 |
| tells Ron no | sits | Darren | day 4, for talk | day 4, Charged | day 4 | the real book | ended (refused) | 7 of 41 |
| tells Ron no | sits | nobody | never | no | day 3 | the real book | ended (refused) | 7 of 41 |
| tells Ron no | sits | no window | never | no | day 3 | the real book | ended (refused) | 7 of 41 |
| tells Ron no | stands her up | Sheila | never | no | never | the day-book | ended (refused) | 7 of 41 |
| tells Ron no | stands her up | Darren | day 4, for talk | day 4, Charged | day 4 | the real book | ended (refused) | 7 of 41 |
| tells Ron no | stands her up | nobody | never | no | day 3 | the real book | ended (refused) | 7 of 41 |
| tells Ron no | stands her up | no window | never | no | day 3 | the real book | ended (refused) | 7 of 41 |

**The wait's stops, first row** (takes the envelope, sits with Ada, Sheila sees
the window):

| day | time | why | line |
|---|---|---|---|
| day 1 | 20:00 | ron | "Ron's at the door with something for you." |
| day 1 | 20:00 | landing | "They'll be expecting the envelope at the landing after ten." |
| day 3 | 20:00 | ron | "Ron's at the door with something for you." |
| day 3 | 20:00 | landing | "They'll be expecting the envelope at the landing after ten." |
| day 3 | 20:30 | tea | "Ada's pot goes on at nine." |
| day 5 | 09:00 | ellis | "DS Ellis is on Quay Street, asking after you." |
| day 5 | 20:00 | ron | "Ron's at the door with something for you." |
| day 5 | 20:00 | landing | "They'll be expecting the envelope at the landing after ten." |
| day 7 | 09:30 | sheila | "Sheila's waiting for you in the office this morning, on her day off." |
| day 7 | 20:00 | ron | "Ron's at the door with something for you." |
| day 7 | 20:00 | landing | "They'll be expecting the envelope at the landing after ten." |

**Row by row, for the port.** PerceptionGolden's rows, with `--awaiting-port`
for the fixes of 30 September.

**Rerun the reference** whenever the Core changes:
`dotnet run --project ledger/TownReach -c Release -- --cast production/specs/hook-cast.json --week-waits`.
The town updates this table when a Core change moves a row, and says so under
Handovers.
