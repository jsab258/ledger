# The hints, each the first time it matters

Town list 6y. Settled as written, 29 September (DECISIONS). Design:
game-design/first-moments-2026-09-29.md. Code:
ledger/Assets/Scripts/Core/FirstMoments.cs.

**What the player gets:** one short hint at the moment it is first of use:
- how to walk, if he stands still;
- how to talk, once Sheila's walk-round ends;
- the coat, when Ron hands it over;
- being seen, the first time someone sees a deed;
- being talked about;
- the Ledger.

Each is shown once, never two at a time.

## Wire it

1. **When he gets control of a new game or a load:**
   `hints.Begin(realSeconds, newGame, savedHintsOrNull)`. Real seconds come from
   the platform clock; one the game restarts at a load is taken up.
2. **On his first step:** `hints.Moved(realSeconds)`.
3. **Each time a moment occurs:** `hints.Happened(moment, realSeconds)`. The
   moments are:
   - `CanTalk`: the walk-round ends (`DayOne.WalkRoundEnds` calls it);
   - `FirstAsk`: Ron hands him the coat;
   - `SeenAtDeed`;
   - `OverheardAboutHim`;
   - `LedgerOpened`.

   Show what it returns at once, if anything.
4. **Each frame:** show what `hints.Due(realSeconds)` returns, if anything.
5. **Showing one:**
   - put its `Key` through `FirstMoments.Fill(text, bindingFor)`, which fills
     {Move}, {Talk}, {Coat} and the rest from his key bindings;
   - show its `Line` in Sheila's or Ron's words when they are with him, as plain
     text until their voice passes the accent gate.
6. **Session record:** a `hint` line (`moment`) each time one shows
   (production/specs/session-record.md).

## Port

`FirstMoments` (Begin, Moved, Happened, Due, Fill, ToJson, FromJson) and its
`Words`. Match the rows behind `--awaiting-port`: `HintDue`, `HintHappened`,
`HintSave`, `HintAfterLoad` and `HintFill`.

## Save

`hints.ToJson()`, already inside `TownSave.Hints`.

## Walk it

1. Start a new game and stand still for four seconds: the walking hint.
2. After Sheila's walk-round: the talk hint, with the talk key filled in.
3. On the first ask night, when Ron hands over the coat: the coat hint, at
   once, in Ron's words.
4. Save and load: no hint shown before shows again.
