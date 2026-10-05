# The friends' evening across a restart, re-run, 5 October 2026 (phase 0's exit review, point 11)

The fresh reviewer of phase 0's exit found that the evening's limit across a restart was last proved on 3 October (production/playtest/friends-account-2026-10-03.md), before tools/friends/evening.ps1 was rewritten on 4 October for his own account, and that the Shipping launch went through a copy of the friends' shortcut rather than the one evening.ps1 makes. Both re-run here, on his account, with real talk.

## How

- `tools/friends/evening.ps1 -Start -CapUsd 0.10`: the evening's file beside his key (`{"capUsd":0.1,"spentUsd":0}`) and "Quay Street (friends)" on the desktop, its target the played copy (F:\LedgerTools\played-game, a Development build of 47cdcf834), its argument the friends' own save folder.
- The game started from that shortcut itself: `tools/ai-tester/play.py start --shortcut "<Desktop>\Quay Street (friends).lnk" --real-talk` (the option added today: the shortcut's own target and arguments passed through untouched, only a window added so the tester can steer). Command line, as the run printed it: `"F:\LedgerTools\played-game\Windows\LedgerProbe.exe" -EncounterSave="F:\LedgerTools\friends-evenings\save" -windowed -ResX=1280 -ResY=720 -nosplash`.
- Runs production/playtest/ai-tester/2026-10-05-1717 and -1722 (pictures on disk only); talk transcripts F:\LedgerTools\tmp\builder\real-talk\2026-10-05-1717 and -1722.

## What happened

1. **Run 1.** The title from the shortcut, with no Continue (the friends' save was empty). New game; Sheila's walk-round; "Talk to Sheila": "Afternoon, Sheila. Busy today?" She answered "Quiet enough." through the checked path in 5.4 s. The evening's file then read 3.6 cents spent. Quit the game from its own menu (Stop press, Quit the game, confirmed); the game and its talk program closed. The file still read 3.6 cents.
2. **Run 2, from the same shortcut.** The title offered Continue, "Monday, 10.04 am, Quay Street" (the friends' save, apart from his; preview phase0-evening-continue-from-shortcut-2026-10-05.jpg), and the street resumed beside Sheila. Two more checked lines took the evening from 3.6 to 8.2 and then 9.4 cents: it started from what it had spent, not from a fresh cap.
3. **At the cap.** The next line was refused before any call was sent (answered in 2 ms, the spend unchanged at 9.4 cents), and Sheila gave her written brush-off, "Not now. I've the books open." (preview phase0-evening-refused-at-cap-2026-10-05.jpg). Quit from the menu again.
4. `evening.ps1 -End`: "The evening spent US$0.09"; the evening's file removed; one row in F:\LedgerTools\friends-evenings\evenings.jsonl (2026-10-05 17:25, cap 0.10, spent 0.094262: this test, not an evening of his friends).

Spend: 6.7 cents of calls, 9.4 cents reserved against the evening (production/playtest/talk-runs.jsonl).

## Found on the way

- evening.ps1 announced every evening as "a five-dollar evening", whatever its cap: it now says the cap and the spend the file holds.
- Known already (FINDINGS.md, 3 October): the first letter typed into a just-opened talk box lands at its end; the game received "fternoon, Sheila. Busy today?A". Sheila's answer was sensible.
- The notice when the cap is reached reads "Live talk cannot be reached just now"; for a friends' evening at its cap the cause is the cap, not the network. Left as written: the brush-off is the ruled behaviour, and the notice is honest that live talk has stopped.
- His Task Manager, set to stay on top, took the front twice; the last key press still reached the game each time.

## Still not done

The shortcut evening.ps1 makes points at the played copy, a Development build; the Shipping package is launched from it only when phase 4 freezes Shipping into the played copy (production/friends-build/MAP.md).
