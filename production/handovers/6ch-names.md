# What the town calls him

Town list 6ch (the rest of 6s, how they know him, is wired). Decided by the
town, 29 September. Design: game-design/what-they-call-him-2026-09-29.md.
Code: ledger/Assets/Scripts/Core/PlayerIdentity.cs and the talk program.

**What the player gets:** canon's ladder, by knowing:
- "the new owner" until they know his name;
- "Nowak" once he gives it or the street has passed it on (Mickey's own people
  know it from the start);
- "Tom" after two days of talk since then, or at once if he asks;
- never back down.

Sheila names him only once she trusts him.

## Wire it

1. **Send nothing for `calls`:** the talk program works the name out and says
   it in each reply's `calls`. Send `calls` only when the game decides
   otherwise; the talk keeps it from then on.
2. **In each line's `acquaintance`:** add `"knowsName": true` once
   `PlayerIdentity.HoldsHisName(theirGossiper)`, meaning they hold the street's
   story of his name. Keep sending `met` and `heardOf` as now; `met` also from
   Sheila's walk-round.
3. **When a reply carries `"gaveName": true`:** call
   `new PlayerIdentity().NameTold(mill, who, now)`. They then hold his name as a
   plain street fact, and the town's rounds pass it on.
4. **Session record:** a `calls` line (`who`, `name`) when a reply's `calls`
   first takes a name, or a new rung.

## Port

Only the Core part: `PlayerIdentity.NameTold`, `HoldsHisName` and `IsNameStory`.
The name story must never be the strongest story in `StreetVoice.RegardFor`, in
an overheard `Exchange` or in `ArrivalLine`, so it never shows in anybody's
manner. Match the rows behind `--awaiting-port`: `NameStoryIs`, `NameTold`,
`NameRegard` and `NameArrival`. The ladder itself runs in the talk program,
which the build machine already rebuilds on every push.

## Save

Nothing new. The talk keeps each person's rung in the talk's own save, and the
name story is in the gossip mill's save.

## Walk it

1. Talk to Ada on day 0 without giving a name: "the new owner".
2. Say "I'm Tom Nowak, Mickey's nephew.": she says "Nowak" from then on.
3. Talk to her on day 1: "Tom".
4. Darren says "Nowak" from the first line, and "Tom" when asked ("Call me
   Tom."). Sheila says "the new owner" until she trusts him.
