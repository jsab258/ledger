# The first Shipping launch, 5 October 2026 (phase 0, item 0.6)

PLAN.md: "One Shipping launch from the shortcut on his own account, first-run preparation included; no second account." Research first: production/research/shipping-build/NOTE.md.

## The build

- `RunUAT BuildCookRun -clientconfig=Shipping`, the build machine's command otherwise unchanged, from main at 1741236 (the build machine's verdict for 405c18c: probeTest PASS), archived into ue-probe/Packaged (a build folder under production/retention.json): 4.5 GB, 4.7 minutes, BUILD SUCCESSFUL.
- First try refused in four seconds: `bUseLoggingInShipping` cannot be set with the installed engine's shared build environment. Dropped; a Shipping copy keeps no log (the target file says why).
- Beside it, as the build machine places them for the played copy: the talk program (LedgerTalk, copied from the played copy, unchanged since 2aab60b) and the voice (a link to F:\LedgerTools\voice-portable).

## The launch, through the shortcut, on his own account

A copy of the friends' shortcut ("Quay Street (Shipping test)", target the Shipping copy, `-EncounterSave` its own folder), opened as Explorer opens a double-click (ShellExecute), the whole screen filmed every two seconds (F:\LedgerTools\tmp\builder\shipping\first-launch; preview production/previews/phase0-shipping-first-launch-2026-10-05.jpg):

- 5 s: black while the game starts.
- 13 s: "Getting the street ready for this PC's graphics card", with its progress line (the first run's shader preparation: basic 2).
- 26 s: "Finding the picture this PC can keep smooth" (the picture ladder).
- 47 s: the title, full screen: New game, Settings, Credits, Quit; no Continue on a first start (basics 3 and 5).
- His Task Manager window stayed on top throughout; it is his, set to stay on top.

## Played, by the AI tester (tools/ai-tester/play.py --packaged, --plain, --real-talk at a $0.50 cap)

Runs production/playtest/ai-tester/2026-10-05-1119 and -1123 (pictures on disk only):

- New game: Sheila's walk-round lines, then the first-steps hint and the first instruction (basics 6 and 7).
- Beside Ron, the prompt "Talk to Ron" (basic 8); one line typed: "Morning, Ron. Quiet today?". He answered "Quiet enough, boss." through the checked path in 6.5 s; the check took three invented details out of his longer draft (F:\LedgerTools\tmp\builder\real-talk\2026-10-05-1119\talk.jsonl; preview phase0-shipping-ron-answers). About five cents of the measuring allowance.
- The Shipping game started its own talk program and its own voice beside it (LedgerTalk.exe and the voice's python.exe, both from the Shipping copy's folder; basic 1).
- Esc: the pause menu ("Stop press": back to the street, the Ledger, settings, quit to the title, quit the game), with the last autosave at 11.00 am game time (basic 19); quitting asked for confirmation. The game then closed cleanly (its pipeline cache written at shutdown, no crash report); his Task Manager had taken the front, so whether the last key press reached it is not certain.
- Restarted: the title offered Continue, "Monday, 11.00 am, Quay Street", and the game resumed beside Ron at Mickey's window, as saved (basic 20; preview phase0-shipping-continue).

## The evening's limit across a restart

Proven on the finished game on 3 October (production/playtest/friends-account-2026-10-03.md, build 2aab60b): an evening kept its 4.8 cents of spend after the game closed, and an evening at 9.8 of its 10 cents refused the next paid line with Sheila's written brush-off. The talk program has not changed since 2aab60b, and its own tests (EveningCap, checking under the cap) run in every build; not repeated with real money today.

## Faults a friend would see, found on the way

1. The pause menu shows "The Ledger: Tom's notebook is not in this build yet": an unfinished feature named to a friend (the map's "nothing a friend sees unfinished").
2. Dark smudges across Ron's white shirt (the base layer) beside Mickey's window.
3. Already known: the white base layer itself, the stand-ins.

## Not done

The launch was from a copy of the shortcut pointing at the Shipping copy on C:, not from the desktop shortcut evening.ps1 makes, which points at the played copy; phase 4 freezes the Shipping package into the played copy and walks the real shortcut. No weaker graphics card was tried (basic 4).
