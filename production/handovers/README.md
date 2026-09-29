# The town's handovers, one card each

For the builder (town list T2, Jafar, 29 September evening: every handover
still waiting, made small, tested and clear, so it can be wired quickly). Each
card says the same five things, and nothing else:

- **What the player gets**, in one line.
- **Wire it:** the calls, in the order play makes them, with the moment of each.
- **Port:** what goes into C++, and the rows behind `--awaiting-port` in
  ledger/PerceptionGolden it must match.
- **Save:** what the game keeps.
- **Walk it:** what the AI tester should see, once it is in.

The line under Handovers in NOW.md stays, one line pointing here. An item is
done only once it is wired and the AI tester has walked it (Jafar, 29 September).

## In the order the first hour needs them

1. [Day one: Sheila's walk-round, and the street's first talk of him](6cg-day-one.md)
2. [The hints, each the first time it matters](6y-hints.md)
3. [The outfit's ask: Ron, the envelope, the landing](6z-the-ask.md)
4. [What the town calls him](6ch-names.md)
5. [Day 3: Ada's tea](6bg-adas-tea.md)
6. [A way to wait, and the clock](6ci-the-wait.md)
7. [Sheila's trust, and the week's end](6ca-sheila-and-the-week.md)
8. [After a deed: the damage, the police, DS Ellis, an arrest](6ar-after-a-deed.md)
9. [The street's own talk: two hours without repeats, and the hush after a deed](6o-the-streets-talk.md)
10. [The town's own news: the one sample](6aq-town-news.md)

Still Jafar's before it can be wired: what a threat does (town list 6cd, on his
30 September page); its line stays under Handovers.

The town's pieces are saved together as one `TownSave` (town list 6bl), its
`ToJson` beside the game's save and `FromJson` on a load: the hints, the asks,
Ada's tea, the police file, what he has heard, the news filed, the damage, the
arrests, the hours the town has talked, and the week's end. Its port matches
the rows behind `--awaiting-port`: `TownSaveWritten`, `TownSaveBack`,
`TownSaveSame`, `TownSaveLaterRefused` and `TownSaveJunk`.
