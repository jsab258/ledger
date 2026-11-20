# Night walk 2026-11-20: diagnosis

Read-only diagnosis. Nothing was fixed, run or committed.

## The measure

The measure is sound. The game's own log shows that the run took Quit, so "no street line within 60 s" is a true failure, not a fault in the check.

## (1) Why the walk never left the title

**Cause:** The Enter key was sent and reached the game, but Quit was the selected choice, so the game closed.

- Game log (F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Logs/LedgerProbe.log): line 1089 "LedgerTitle: shown, no saved story" (no Continue entry, same four choices as 19 Nov). Line 1380 "LedgerTitle: chose Quit" at 01:55:25. Lines 1381-1416 show the engine exiting.
- walk.log, 01:55:26: "press: aiTester status=NOT-IN-FRONT front=...cmd.exe". This message comes from picture() (tools/ai-tester/play.py:433), which runs after the key is tapped (play.py:687, 745). The "(no keys sent)" form at play.py:660 was not printed, so the key did go in. The console came to the front because the game had already closed. It is a result of the quit, not the cause. No firewall box and no clipboard panel was involved.
- step-001.jpg is the "started" picture, taken before Enter. It already shows Quit in hand.

**How Quit got the keys:** No code changed between the two nights. The diff 5652a99..5eb76d5 touches no ue-probe/Source, no TitleScreen.cpp (last changed 24 Oct) and no walk tools. FocusFirst gives New game the keys (TitleScreen.cpp:108-136). The per-tick refocus only runs when the focused widget is not one of the menu's own choices (TitleScreen.cpp:704). A choice also takes the keys when the mouse enters it (LedgerPaper.cpp:571-576, OnMouseEnter calls SetUserFocus). The title shows the pointer (log line 1088, bShowMouseCursor True; DoNotLock). Slate sends a synthetic cursor move every tick even when the mouse is still (engine SlateApplication.cpp:1800-1805; SlateUser.cpp:720-745, "the UI can change even if the mouse doesn't move"). So a pointer resting where the Quit row is drawn gives Quit the keys, and the walk's one Enter (route_walk.py:588) takes it.

**Confidence:** high that Enter took Quit. About 80% that the resting pointer is how Quit got the keys: it is the only path the code allows without a key press, but the pointer's position was not recorded.

**Would confirm it:** log the cursor position and window rectangle at play.py start, or launch once with the pointer placed over the Quit row.

**Smallest fix (not applied):** in the game, OnMouseEnter takes focus only on a real mouse move (cursor position differs from the previous one). Alternatively, the tester puts the pointer in a neutral spot before the first picture. The walk could also report the log's "chose X" line.

## (2) The barefoot person in the white base layer

**Not new, and not Ron's held rows.** The same woman stands at the same spot in the 18 Nov and 19 Nov step-001 pictures. Log line 1331: "Lena is undressed (the base layer shows)". Lines 1324-1330 show SheilaCardigan, SheilaBlouse, SheilaSkirt and SheilaShoes held back (production/specs/garments.json, rows with "hold" at lines 136, 170, 194, 217; held since commit ff2e38743, 11 Nov). She wears only SheilaHandbag, the bag visible in the picture. FINDINGS.md:23 already lists "the cast still wear the white base layer". RonWorkTrousers and RonJumperOverTrousers replace rows only under -WearHeld (LedgerGarments.h:283-303 and 309-318). The walk passes no -WearHeld, and no Rocco garment line was logged before the quit.

**Confidence:** high.

## Not reached

- The pointer's position at 01:54.
- The build machine's run output (not on disk).
- The scheduled task's console window.
- The installed engine is 5.8.4 (Build.version), not the stated 5.8.2. The lines cited are from 5.8.4.
