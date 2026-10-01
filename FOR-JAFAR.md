# For Jafar

The overview first (the builder keeps it, for all three sessions); then each
session's own dated summary, under 200 words. Earlier summaries are in git;
everything before 24 September afternoon is in
production/archive/FOR-JAFAR-to-2026-09-24.md.

## Overview (Thursday 1 October, 05:35)

### Needs you

(Every page's stored answers checked at 03:30: Thursday's and Wednesday's, mine; the town's; the clothing session has no page.)

1. **[The town's page](https://claude.ai/artifact/3dS6bihBQhirakfkSo9zNz), three taps.** Does seeing Tom break a window send a neighbour to the police? Recommended yes (today nobody ever reports). Sheila on the faster model? Recommended try it, blind-checked (her first sentence 0.81 s against 1.43 s, measured outside the game). The other characters' street lines: one more try, a new way? Recommended try once.
2. **The route is ready for your cloud review:** main as of 760832bce, green on the build machine at 01:08 (its Core tests and the full Unreal run); what changed and the runs in the finished game before and after are in production/playtest/review-runs-2026-09-30.md. Recommended: run it.
3. **[Thursday's page](https://claude.ai/artifact/3zqyXtiTA35rPcuufuD48K), three taps.** The voice's delay: down from 4 s to 3 s of voice work for a short line in the game; every faster way I built runs at half speed beside the game. Recommended: this week's other items first, then research and move the voice into the game itself (about two weeks). And Ron's and Darren's thinking sounds with two kinds of face, blind: which looks like them saying it?
4. **[Wednesday's page](https://claude.ai/artifact/Gbu86NurpJTnXCca6vsGAJ), four looks still open since Wednesday morning:** the street by day and at night, their mouths moving as they speak, Ron's boots and Sheila's handbag. (Its hair call is settled by your Darren S6 and Sheila S4 picks.)

### Road to worth playing

(Your list of 30 September, after the audit: the playable route first; other visual work stopped while it is broken.)

- **One continuous route through ordinary play** (builder the game side, town the Core side): READY FOR YOUR CLOUD REVIEW (Needs you), not done until it passes. Every High fault of your reviewer's and the smaller ones fixed, a failing test first for each, the town's half ported, and the review's three runs played again in the finished game, all passing; C5's small save items remain. Since yesterday: ready for review.
- **The delay before a character speaks** (builder, item 2): SET ASIDE, your decision (Thursday's page). On the real path the words come at 1.9 s (30 lines, 30 September); the voice's work for a short line in the game is now 2.98 s (was 3.95; its decoder on the graphics card, the same sound), so the first sound is about 4.5 s after Enter, covered by the characters' short sounds. Tried tonight and failed in the game: the voice in pieces inside the sentence (1.0 s to the first piece on the idle PC, slower with gaps in the game) and a compiled main loop (faster idle, slower in the game); frame caps, half resolution and priority changed nothing. Beside the running game every way runs at half its idle speed. Since yesterday: 1 s off, then set aside past the two-tries rule.
- **Replies that say "that's all I know"** (town): about half of a newcomer's questions by the audit's count (31 to 38 of 60); the town's latest run, 23 of 60. Since yesterday: fewer, not solved.
- **Replies that time out** (town, measured in play by the builder): none of 30 on the real path in the finished game this evening (29 in the character's own words, 1 ended the talk). Since this morning: measured in play.
- **A release on a clean machine** (builder, item 3): the voice's stopgap tried and working: today's voice program packed into one folder (4.3 GB: its Python, torch and Nano's weights) runs with nothing installed behind it, passes its self-checks and speaks a line (on the processor here, slowly; on the card as fast as today). About a day more to a friends' build (the game finding it by itself, a fresh-account test); no money, all free licences. The proper conversion stays about two weeks by the note and the route for release. Since this morning: your ruling, and the stopgap proven.
- **Faces** (builder, item 4): frozen. Ron's and Sheila's are final; Darren's S6 is your pick, and you see it once at full size before it is final. Since yesterday: frozen.
- **Voices** (builder): Ron's and Darren's yes; Sheila's p267 your yes, with your note that it sounds flat, as Ron's first take did. The cloud research's voice-direction note says why: the clips they learn from were read, not acted; its method (a clip library per mood, direction for every line, many takes, chosen by ear in the game) is how they get worked next. Since yesterday: the method.
- **People dressed** (the clothing session makes, the builder fits): Ron's boots and Sheila's handbag in the game; suits and coats by your ruling (MakeHuman's, skinned); the suit jacket to be filmed in the game (the list's last item). Since this morning: your rulings.
- **The AI tester walking it** (builder; functional tests of the package are item 8, by the packaged-testing note): walked the route today in the editor and the packaged game, five runs, and found the faults fixed this afternoon. Since yesterday: the whole route walked, reload included.

## Town, 1 October

**[Your page](https://claude.ai/artifact/3dS6bihBQhirakfkSo9zNz):** three taps. Does seeing Tom break a window send a neighbour to the police? (I say yes.) Sheila on the faster model? (I say try it, blind-checked.) The other characters' street lines: one more try, a new way? (I say yes, once.)

**Your review's Core side:** all fixed and ported, each test first:
- Sheila asks on Monday if he misses Sunday (seen in the game);
- DS Ellis asks only on Quay Street;
- a full sighting is certain;
- your ruling: a noise or a shape is never "he did it";
- Rita finds her own window;
- Ada's tea as she'd tell it;
- the town's talk in time;
- a no across one o'clock.

Three checks found faults in my fixes; all mended.

**Set aside after three reviews (past the two-tries rule):** the other named characters' street lines; the shared lines stay.

**Talk delay:** words 1.9 s after Enter, the check about 1.1 s of it. Sheila's first sentence 1.43 s; caching nothing; the faster model 0.81 s.

**Your key:** $0.18 today, logged.

**Research:** cutting the first words' delay.

**C: free:** 56.3 GB, 63.4 now. Backup runs with this commit.

**Next:** your three taps.

## Clothes, Thursday 1 October

(Written 30 September, 16:00; nothing has changed since.)

**Needs you (scope), no page:** your rule set aside both jackets, so the list cannot move. (A, recommended; carrying on with it) the builder tests the suit jacket in Unreal, cloth on, when his route allows; nothing reaches your page until it passes there and at the gate. (B) park clothing until his route runs. (C) a paid Fab jacket, $5 to 20, against your ruling of this morning.

**Made:** the jacket the game way: a clean mesh laid on its pattern, textures baked, skinned, joints fixed, carried to Darren; then MakeHuman's free suit jacket fitted on a tailor's form of each man.

**Set aside:** the donkey jacket (three reviews: a padded look); the suit jacket (three: Ron only two small breaks, at the lapel's end and under the collar; Darren barrel-shaped).

**Research:** retopology and skinning; carrying garments and seam faults; fitting to a form, not the skin.

**Pushes:** free tests only. **C: free:** 51 GB at the start, 46 now (my scratch is all on F:). Backup ran: OK.

## Builder, Thursday 1 October

(Written 1 October, 03:45.)

**[Thursday's page](https://claude.ai/artifact/3zqyXtiTA35rPcuufuD48K):** one tap, the voice's delay. I recommend your other items first, then the voice moved into the game.

**The route: ready for your cloud review** (main as of 760832bce): every High fault fixed; the review's three runs pass in the finished game.

**The delay:** the voice's work for a short line in the game fell from 3.95 to 2.98 s (its decoder on the graphics card, same sound). With the words at 1.9 s, the first sound comes about 4.5 s after Enter.

**Failed, past two tries:** the voice in pieces (1.0 s to the first piece on the idle PC; slower, with gaps, in the game); a compiled main loop (slower in the game); frame caps, half resolution, priority: no change. Set aside; your call.

**Evidence:** checks 38/38; Core tests green on GitHub.

**Got wrong:** Wednesday's four open looks were missing from Needs you; back on.

**Research:** fast first sound (a helper); the voice in pieces in the game (mine).

**C:** 64.9 GB last night, 60.5 now (Windows' page file grew under the game-and-voice runs). F: 8 GB. Backup with this commit.

**Next:** the friends' build, short of the new account.

## 26 September, day

**[The weekend page](https://claude.ai/artifact/XbMbZdQo9DwXf9NurNi3rR):** one face passed the gate, Ron's P2. Is he Ron?

**Faces.** Five each, from northern European presets. The street's daylight causes the East Asian look: the same faces read English in plain light. Only Ron's P2 passed the blind reviewer; Sheila and Darren failed twice: set aside.

**Delay, your line to the first sound (median / slowest):**
- Before: 6.2 / 7.8 s.
- After, in the game: 5.4 / 8.7 s. Words at 1.4 s; the voice takes 4 s more.
- Pocket TTS: 2.0 / 2.9 s, but all three voices drifted American, twice: set aside.

**Free space on C:.** 64.9 GB at the start, 49.8 GB at the end (Unreal's caches): cleanup page first next. Backup OK.

**Got wrong.** Every candidate's eyes came out green (I misread Epic's eye chart). One call broke the build machine's build; fixed.

**Missing.** Your latency research.

**Decide.**
- Street daylight: (A) brighten it toward the concept sheet (recommended), (B) leave it.
- Speed: (A) retry Pocket from longer approved takes (recommended), (B) keep 5.4 s.
- Desktop "UPDATE FROM CLAUDE": (A) delete it yourself (recommended), (B) I repoint it.
