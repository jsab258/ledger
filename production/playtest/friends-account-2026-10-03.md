# The friends' build in a fresh Windows account (3 October 2026, P5)

Jafar's order of 3 October: "P5: start the friends' build in a fresh Windows account, voice and talk included. For the evening, a copy of my key is placed in that account and removed afterwards." His ruling: "my friends may talk on my key during the friends' evenings, capped at five dollars an evening."

## What was missing, and what is in place now

1. **The key.** The game reads it from the signed-in account's own folder (AppData\Local\LEDGER), so a fresh account had none.
   - **tools/friends/evening.ps1 -Start,** run once as administrator from his account, copies his key into the friends' account.
   - It also writes a five-dollar evening beside the key and puts "Quay Street" on that account's desktop.
   - **-End** writes down what the evening spent (F:\LedgerTools\friends-evenings\evenings.jsonl) and removes the key and the evening, checking they are gone.
2. **The five dollars were a game start's, not an evening's.** A restarted game began again at zero.
   - The talk program now starts from the evening's file and keeps the spend in it as it goes.
   - A damaged file leaves the talk offline, never uncapped.
3. **The voice.** Today's voice needs Python and its weights, installed only in his account.
   - The portable voice (F:\LedgerTools\voice-portable, 4.3 GB, nothing installed) is remade.
   - The build machine now links it in as the played copy's Voice folder after every new build (first done at 15:27 today).
4. **The saved game.** The played copy keeps its save inside its own folder on F:.
   - That save is shared between accounts (the tester's game showed under Continue) and is lost with each new build.
   - The friends' shortcut now gives them their own save folder in their account.
   - His own play still saves in the shared folder (FINDINGS.md).

## Played as a fresh account would play it

The AI tester played the finished game of 2aab60b (the build machine's package and its played copy) as a fresh account would (tools/ai-tester/play.py --profile):
- its own empty user folders;
- nothing of his account's on the path, no Python;
- the game's own talk program and voice beside it;
- a copy of the key and an evening placed as the script places them, the evening ten cents instead of five dollars.

Results:
- **Talk and voice:** the game used its own talk program, live on the key, and its own voice. Sheila's reply was checked; words at 3.74 s, first sound at 4.39 s.
- **The evening kept its spend:** 0 before, 4.8 cents after the game closed.
- **And started from it:** an evening at 9.8 of its 10 cents refused the first paid call, and Sheila said her written brush-off ("Later. I'm in the middle of something."). A fresh cap would have let it through.
- **The first launch in a new account** prepares the graphics before the street ("4852 to go"): **96 s** after New game. The next start was quick.
- **The key and the evening were removed** afterwards: checked gone.
- **Spent:** $0.048 (production/playtest/talk-runs.jsonl). The day's measurement total is $0.71 of the dollar.

## Not proven here

- A real second Windows account. Making one is his: the session may not create accounts.
- The stand-in shares this account's graphics driver and permissions. F: is open to every signed-in account (read and change), so the played copy and the voice should open from the friends' account.
- Only a real account shows how long the graphics take there the first time, and whether the voice starts on the graphics card in it.

## His steps, about ten minutes at the PC

1. Settings, Accounts, Other users, Add account: "I don't have this person's sign-in information", then "Add a user without a Microsoft account". Name it Friends.
2. Sign in to Friends once and sign out, so Windows makes its folder.
3. In his own account, open PowerShell as administrator and run:
   `powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\Jafar\ledger-local\tools\friends\evening.ps1 -Start`
4. Sign in to Friends, double-click Quay Street, and wait about a minute and a half the first time. Start a New game, press T beside Sheila and say hello. She should answer and be heard.
5. After the evening, back in his account, the same command with `-End`. It says what the evening spent and removes the key.
