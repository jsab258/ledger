# Day 3: Ada's tea

Town list 6bg. Settled as written, 29 September (DECISIONS). Design:
game-design/day-three-2026-09-29.md. Code: ledger/Assets/Scripts/Core/FirstWeek.cs
(`AdasTea`).

**What the player gets:** on the evening of the outfit's second ask, Ada asks
him in for a pot of tea at nine. His choice leaves something with her:
- He sits with her and she warms to him.
- He comes late or leaves early.
- He stands her up and she cools on him, which can later send her to the
  police about what she saw.
- If he slips off to the landing, she sees him go from her window.

## Wire it

1. **On the morning of the second ask's day** (the first ask's day plus two):
   `tea = AdasTea.For(firstAskDay, hasMetAdaByThen)`. It is null if he has not
   met her: she does not ask a stranger in.
2. **The first time Ada sees him that day before nine:** `tea.SheSeesHim(now)`
   gives her line. Show it in her words; she asks once.
3. **From nine to eleven:** `tea.WithHer(now)` for every game minute he is in
   her house, skipped time included. Her door is in the terraces across from
   Mickey's.
4. **At eleven:** `tea.Close(adaGossiper, now)`. It judges the evening from the
   minutes:
   - Stayed: there by half nine, still there at half ten, never away more than
     ten minutes;
   - LeftEarly;
   - StoodUp.

   It changes her regard and gives her a memory.
5. **When he sets off for the ferry landing that night for the ask, or reaches
   it, up to one in the morning:** `tea.WentToTheLanding(mill, now, true)`.
   She sees him go, once.
6. **Session record:** a `tea` line (`day`, `state`: Stayed, LeftEarly or
   StoodUp) when it closes (production/specs/session-record.md).

## Port

`AdasTea` (For, SheSeesHim, WithHer, Close, WentToTheLanding, ToJson,
FromJson). Match the rows behind `--awaiting-port`: `Tea`, `TeaAsked`,
`TeaBefore11`, `TeaClosed`, `TeaSeenGoing`, `TeaSeenGoingOnce` and `TeaSave`.

## Save

`tea.ToJson()`, already inside `TownSave.Tea` (null before it is made).

## Walk it

1. Meet Ada on day 1 or 2. On day 3 before nine she asks him in.
2. Go at nine and stay till half ten. The next time they talk she is warmer.
3. In a second run, stay away. She says she'll not ask again, and her talk of
   him cools.
