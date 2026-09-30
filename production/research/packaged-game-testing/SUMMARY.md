# Testing the finished game the way a player plays it

Research, 30 September 2026, by a separate research helper. (The helper returned its text; the session that asked for it saved it here after checking its claims about the project's own files.)

## What professionals do, in order

1. **Quick code tests on every change.** LEDGER already has these (the tens of thousands of checks).
2. **A start-up check on every packaged build.** Does the finished game start, reach the street, close cleanly, and leave no crash or error behind? Epic supplies a free test runner that starts the packaged game, watches it, collects its log and any crash, and gives a pass or fail.
3. **A scripted walk of the main route**, sometimes called the golden path. The same route is played the same way each night. It checks the things a player would notice, one by one.
4. **Long unattended runs** to catch rare crashes and slowly growing memory, plus **performance recordings** on a fixed route.
5. **Free play by people**, and more and more by AI agents, looking for anything nobody thought to script.

Big studios mostly drive their games from inside the game. Ubisoft's bots for The Division press the player's controls in software, and Rare's tests call the game's own code. Only real key presses coming through Windows catch bugs like typing into the conversation box also walking Tom. That bug sat between the keyboard and the game, and in-game driving goes around that layer.

## What fits a one-person project

Everything needed is free and mostly already on the PC: Epic's test runner, the key-pressing tool the AI tester already uses, and a free outside frame-time recorder. Paid testing products (GameDriver, AltTester, the AI-agent services) add nothing essential here. Their free tiers come with conditions, and they need their own plug-in built into the game.

## Recommended setup, in order

1. **Start-up check** after every packaging run. It is small, and half of it exists.
2. **The scripted route played with real key presses.** It uses the same keys, mouse and typing as the AI tester, following a fixed script. The game writes one plain line each time a stage is reached, such as the crime committed, the witness speaking or the reload landing in the right place. Each stage has its own time limit and a picture. It gets written expectations in plain words, separate from the stored results: for example, "typing in the talk box never moves Tom" and "after a reload Tom stands where he saved".
3. **The AI tester's free walk** on the packaged game. One catch: the game clock runs two game minutes per real second, and the tester thinks for several seconds between moves. Research benchmarks pause the game while the AI thinks. We should do the same where the build allows it, or else read clock oddities with that in mind.
4. **Frame times recorded from outside the game**, which works on any build.

## Which build is tested, and why

Studios run automated tests on a development build. It keeps the log, the console and the test hooks. They measure speed on a "Test" build, which runs like the release but keeps a few tools. They give the release ("Shipping") build a final check. Shipping strips out the console, and by default it keeps no log.

The in-between Test build needs Unreal built from source, and our copy of Unreal almost certainly cannot make it. So yes, split "walk the Shipping build", but like this:

- **Every day**: the start-up check, the scripted route and the AI tester, all on the packaged development build.
- **For each release candidate**: the same route and a thirty-minute walk on Shipping, in the fresh Windows account. For that, the game needs its own small record of what happened, since Shipping has no log. We should also try switching the log back on.

## Two things that need a decision

- Automated runs may never use LEDGER's live-talk key, so a Shipping walk "with the real dialogue" needs a ruling: the stand-in, or real replies written through Claude Code on the subscription, which the project's rules already allow for the few talk checks that need a real reply.
- Real key presses stop working when the PC locks. Night-time runs need the PC left unlocked, or they run in the daytime while it sits idle.

## What could not be verified

- Many sources could not be opened from here, including the talks, the forums, Microsoft's pages and the vendors' pages. For those I had only search summaries, and they are marked as such.
- The engine's own code was out of reach. Three things are unconfirmed until tried once on the PC: whether a Test build is truly unavailable, whether logging can be switched on in Shipping with our copy, and whether Epic's test runner watches a Shipping build cleanly.
- I could not check whether GitHub now charges for self-hosted build machines.
