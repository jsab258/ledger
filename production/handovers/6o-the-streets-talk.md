# The street's own talk: two hours without repeats, and the hush after a deed

Town list 6o and 6an. Settled, 28 and 29 September. Code:
ledger/Assets/Scripts/Core/StreetVoice.cs and RemarkLedger.

**What the player gets:**
- The neighbours' talk he can make out comes at most every 45 seconds.
- He never hears the same line twice in two hours.
- Just after a deed (glass, a shout, a crash), those in earshot react to what
  they heard for ninety real seconds, naming nobody they did not see, then
  settle.

## Wire it

1. **One `RemarkLedger` per player.** Pass it as the last argument of
   `StreetVoice.Ambient` and `Exchange`, and call `ledger.Heard(line)` on each
   line he hears.
2. **Keep `StreetVoice.ClearWordsEverySeconds` (45 s)** as the floor of what he
   can make out. The murmur (`ChatterLevel`) is unchanged.
3. **After a deed:** pass `justNow` (`"glass"`, `"shout"`, `"crash"` or another
   noise) and `secondsSince` (real seconds; below zero for none) to
   `StreetVoice.Ambient` for pairs in earshot. Start one exchange
   `JustNowSpeakAfterSeconds` after the hush, instead of waiting
   `ClearWordsEverySeconds`.
4. **Voices:** make crowd-voice clips for the 45 new just-after lines (banks
   ambient/open/justnow/*, ambient/reply/justnow and ambient/*/settling) and
   re-record the 23 replaced street lines. The old and new lines are in
   production/research/street-lines-1990/. Then run BarkGen.

## Port

`StreetVoice.Ambient`'s last two arguments with `JustNowSeconds`,
`SettlingSeconds` and `JustNowSpeakAfterSeconds`, plus the ledger's
`SpokenLine.Wording` and `StreetVoice.WordingOf`. Copy the seven replaced
exchange lines into StreetVoice.h. Match the rows behind `--awaiting-port`:
`JustNow`, `WordingOf`, `RemarkRecord`, `RemarkKey`, `RemarkFreshRun` and
`RemarkCase`. Then move `EmitJustNow` above the awaiting line.

## Save

`RemarkLedger.ToJson` and `FromJson` (remarks.json beside the encounter's save,
already done).

## Walk it

1. Stand in the street for twenty minutes: no neighbour's line repeats.
2. Break a window at night: those nearby say something about the noise for a
   minute or so, naming nobody, then go quiet.
