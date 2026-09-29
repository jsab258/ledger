# Day one: Sheila's walk-round, and the street's first talk of him

Town list 6cg. Decided by the town, 29 September. Design:
game-design/day-one-2026-09-29.md.

**What the player gets:** in the first minutes, Sheila shows him round in her
own words, and the street starts talking about the newcomer at Mickey's.

## Wire it

1. **At the start of a new game (day 0), before he can walk:** show
   `DayOne.WalkRound` as plain text, stop by stop (door, office, drivers,
   Mickey's door, flat). It is five lines in Sheila's words, and her voice
   waits on the accent gate. He may skip it.
2. **When it ends, played or skipped:** call `DayOne.WalkRoundEnds(hints, now)`
   and count Sheila as met. Her last line is the talk hint's own; the hints
   show it when next asked (`FirstMoments.Due`).
3. **The first time he arrives at Mickey's on day 0:** call
   `DayOne.Arrived(mill, cast, now)`. Everybody at Mickey's then saw him
   arrive, and the town's rounds pass it on.
4. **When somebody passes him with nothing else to say:** ask
   `StreetVoice.ArrivalLine(g, floor, ledger, seed, familiarity, coatOn, hasTalkedWithHim)`.
   Say it only if it returns a line, and record the line heard in the ledger,
   as for any remark. It returns nothing:
   - while he wears the coat;
   - to someone he has talked with;
   - for Sheila or June.

## Port

`DayOne.WalkRound`, `WalkRoundEnds`, `IsArrival`, `Arrived`, and
`StreetVoice.ArrivalLine` with its two banks, recognition/arrival-saw and
arrival-heard. Match the rows behind `--awaiting-port`: `WalkRound`,
`ArrivalSeen`, `RecognitionArrival`, `ArrivalLine` and `NameArrival`. The
arrival is never in `StoryThatShows`, `RegardFor` or an overheard `Exchange`.

## Save

Nothing new. The arrival story is in the gossip mill's save, and the hints in
`TownSave.Hints`.

## Walk it

Start a new game:
1. Sheila's five stops appear, then the talk hint.
2. Walk down the street without the coat. Someone who saw him arrive says
   something like "You'll be Mickey's nephew, then.", once.
3. Talk to that person, then pass them again. There is no arrival line now.
