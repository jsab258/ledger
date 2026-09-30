# For Jafar

The overview first (the builder keeps it, for all three sessions); then each
session's own dated summary, under 200 words. Earlier summaries are in git;
everything before 24 September afternoon is in
production/archive/FOR-JAFAR-to-2026-09-24.md.

## Overview (Thursday 1 October, 00:10)

### Needs you

(Every page's stored answers checked at 00:35: yours, the town's two; the clothing session has no page.)

1. **[The town's page](https://claude.ai/artifact/3dS6bihBQhirakfkSo9zNz), two taps.** Does seeing Tom break a window send a neighbour to the police? Recommended yes (today nobody ever reports). Sheila on the faster model? Recommended try it, blind-checked (her first sentence 0.81 s against 1.43 s, measured outside the game).
2. **The route is ready for your cloud review** once tonight's last push is green on the build machine (about 01:15): main as it stands then; what changed and the finished-game runs in production/playtest/review-runs-2026-09-30.md. Recommended: run it.

### Road to worth playing

(Your list of 30 September, after the audit: the playable route first; other visual work stopped while it is broken.)

- **One continuous route through ordinary play** (builder the game side, town the Core side): NOT DONE, nearly ready for your cloud review. Your reviewer's three runs of the finished game showed every fault it had read, and one it missed (no conversation was ever saved). All the High faults and most of the smaller ones are fixed, a failing test first for each, with the town's half ported, and checked in the finished game: the witnesses are whoever is really there, in that hour's light; only someone who recognised him names him; Continue brings back the conversation; the Z wait stops for Ron and the landing, hour by hour. Left: the town's last Core fix (a late no across one o'clock) and Sunday's question checked in the finished game; then I tell you it is ready. Since yesterday: fixed and walked.
- **The delay before a character speaks** (builder, item 2): MEASURED ON THE REAL PATH, 30 lines in the finished game on your key ($0.23): the words come 1.9 s after Enter (median; 1.1 to 3.8), the first sound 5.4 s (2.2 to 10.2); none within your 2 s. The voice itself is the larger part (3.7 s). Since this morning: measured for real; the fix is the list's next item.
- **Replies that say "that's all I know"** (town): about half of a newcomer's questions by the audit's count (31 to 38 of 60); the town's latest run, 23 of 60. Since yesterday: fewer, not solved.
- **Replies that time out** (town, measured in play by the builder): none of 30 on the real path in the finished game this evening (29 in the character's own words, 1 ended the talk). Since this morning: measured in play.
- **A release on a clean machine** (builder, item 3): the voice's stopgap tried and working: today's voice program packed into one folder (4.3 GB: its Python, torch and Nano's weights) runs with nothing installed behind it, passes its self-checks and speaks a line (on the processor here, slowly; on the card as fast as today). About a day more to a friends' build (the game finding it by itself, a fresh-account test); no money, all free licences. The proper conversion stays about two weeks by the note and the route for release. Since this morning: your ruling, and the stopgap proven.
- **Faces** (builder, item 4): frozen. Ron's and Sheila's are final; Darren's S6 is your pick, and you see it once at full size before it is final. Since yesterday: frozen.
- **Voices** (builder): Ron's and Darren's yes; Sheila's p267 your yes, with your note that it sounds flat, as Ron's first take did. The cloud research's voice-direction note says why: the clips they learn from were read, not acted; its method (a clip library per mood, direction for every line, many takes, chosen by ear in the game) is how they get worked next. Since yesterday: the method.
- **People dressed** (the clothing session makes, the builder fits): Ron's boots and Sheila's handbag in the game; suits and coats by your ruling (MakeHuman's, skinned); the suit jacket to be filmed in the game (the list's last item). Since this morning: your rulings.
- **The AI tester walking it** (builder; functional tests of the package are item 8, by the packaged-testing note): walked the route today in the editor and the packaged game, five runs, and found the faults fixed this afternoon. Since yesterday: the whole route walked, reload included.

## Town, 1 October

**[Your page](https://claude.ai/artifact/3dS6bihBQhirakfkSo9zNz):** two taps. Does seeing Tom break a window send a neighbour to the police? (I say yes.) Sheila on the faster model? (I say try it, blind-checked.)

**Your review's Core side:** all fixed and ported, each test first:
- Sheila asks on Monday if he misses Sunday (seen in the game);
- DS Ellis asks only on Quay Street;
- a full sighting is certain;
- your ruling: a noise or a shape is never "he did it";
- Rita finds her own window;
- Ada's tea as she'd tell it;
- the town's talk in time;
- a no across one o'clock.

Three checks (two fresh reviewers, then the builder) found faults in my fixes; all mended.

**Set aside after three reviews (past the two-tries rule):** the other named characters' street lines; the shared lines stay.

**Talk delay:** words 1.9 s after Enter, the check about 1.1 s of it. Sheila's first sentence 1.43 s; caching nothing; the faster model 0.81 s.

**Your key:** $0.18 today, logged.

**Research:** cutting the first words' delay.

**C: free:** 56.3 GB, 63.4 now. Backup runs with this commit.

**Next:** your two taps.

## Clothes, Thursday 1 October

(Written 30 September, 16:00; nothing has changed since.)

**Needs you (scope), no page:** your rule set aside both jackets, so the list cannot move. (A, recommended; carrying on with it) the builder tests the suit jacket in Unreal, cloth on, when his route allows; nothing reaches your page until it passes there and at the gate. (B) park clothing until his route runs. (C) a paid Fab jacket, $5 to 20, against your ruling of this morning.

**Made:** the jacket the game way: a clean mesh laid on its pattern, textures baked, skinned, joints fixed, carried to Darren; then MakeHuman's free suit jacket fitted on a tailor's form of each man.

**Set aside:** the donkey jacket (three reviews: a padded look); the suit jacket (three: Ron only two small breaks, at the lapel's end and under the collar; Darren barrel-shaped).

**Research:** retopology and skinning; carrying garments and seam faults; fitting to a form, not the skin.

**Pushes:** free tests only. **C: free:** 51 GB at the start, 46 now (my scratch is all on F:). Backup ran: OK.

## Builder, Thursday 1 October

(Written 30 September, 22:50; refreshed by 07:00.)

**No page from me;** the town's page is all answered.

**The route: not done.** Your reviewer's three runs in the finished game showed every fault it had read, and one more: no conversation was ever saved. All the High faults are fixed, a failing test first for each, the town's half ported: the witnesses are whoever is really there, in that hour's light; people keep their day; meeting him lets them recognise him; only someone who knew him names him; talk survives Continue. Also fixed: the Z wait (hour by hour), safer saves, no talk through walls, witness lines that said "half nine" at noon.

**Evidence:** 38 of 38 checks; the port agrees with all 57,770 rows; the build machine passed the first push.

**Failed or unproven:** I broke the Core tests once (fixed in minutes); not yet walked in the packaged game.

**Past two tries:** nothing.

**C:** 45 GB this morning, 64.9 now. F: 8 GB.

**Research:** none new tonight.

**Backup:** with this commit.

**Next:** the packaged walk, then I tell you the route is ready for your cloud review.

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
