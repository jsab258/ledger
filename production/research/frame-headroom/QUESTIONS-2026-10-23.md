# Frame headroom: the questions (23 October 2026, his order of that afternoon)

Phase 1's Exit D failed (production/audits/phase1-exit/CLOSE-D-REVIEW-2026-10-22.md): card memory with the voice 7 to 9.9 GB against 6; the walk's worst frame 87 ms on the repeat, at the same moment every walk; the card's spare time 0.3 to 0.5 ms against PLAN's 1.4 to 2.5. His order: first re-measure card memory now that the voice runs on the processor; then the 87 ms frame and the card's spare time; research first, then fix, measured on the packaged walk.

## 1. Card memory, the voice on the processor
- 1a. On the packaged game with Pocket speaking on the processor throughout, what does the card hold: in all, the game's own, the voice's, and other processes', standing by day, at night and walking? Median and peak, two runs each.
- 1b. Is the PC quiet: what else holds the card while it runs?
- 1c. How is a card-memory budget set and measured professionally (Windows' counters against the engine's own accounting: the texture streaming pool, render targets, Lumen's and Nanite's buffers), and which of those does the 6 GB line mean?

## 2. The first-use stall about 4.2 m into the walk
- 2a. What happens at 5.4 s into every walk: what loads (FlushAsyncLoading, and of what), and which pipeline is first used (PSOMisses=1)? Read from a trace of the packaged walk, not guessed.
- 2b. What is Unreal 5.8's own method for first-use pipeline hitches end to end (PSO precaching, the bundled pipeline cache, their settings and their limits), from Epic's documentation read in full?
- 2c. Which of these is on in this project's packaged build, and why does the miss still happen?
- 2d. The fix, and its measure: the walk repeated at least three times on the package, every frame under 33.3 ms.

## 3. The card's spare time
- 3a. What took the card's spare time from 2.65 ms (7 October, 67c51f5) to 0.28 to 0.54 ms (21 October, 00f81b1)? Pass by pass, from the kept captures.
- 3b. What does a shipped game budget per pass at this resolution and quality, and what can be cut with the least loss to the picture (named, measured)?
- 3c. After any change: the spare time, by day and at night, two runs each.

## Rules
Primary sources read in full, each with its link and the date read; measured where possible; anything unconfirmed marked unverified; anything not reached listed.
