# First smoke run of the AI testers on a real build (4t), 20 Nov 2026

Why: 4t was built, but no AI player or breaker had ever played. One short session each on the round 5 build (the page's current version, rebuilt byte for byte) proves the pipeline before the one-shot's build reaches the first loop. Lane run of 07:16.

What ran: play.py serve (two servers, seeds 7 and 11, 12-minute sessions); one player type, the rusher (Opus, high effort, blind); one breaker, the money cheat (Sonnet). The helpers saw only their brief, the screenshots and the keys. Both sessions ran on briefs refilled by the new launch.py after the fault below was caught before any helper started; no session used a broken brief.

## Pipeline findings (fixed or noted)
- Fixed: filling the briefs by plain text replacement turned LEDGER_PLAY_PORT into LEDGER_PLAY_8771 and left the launcher's own note in the breaker's brief. New tools/lane/prototype/reviewers/launch.py fills each placeholder as a whole word and refuses an unfilled brief (test_launch.py, 2 of 2).
- Pace and cost: the rusher played 2.1 game minutes (quit) in about 6 real minutes, 58 actions; the breaker 4.8 game minutes in about 14 real minutes, 195 actions. A 60-minute evening per player type is therefore hours of real time per helper; the first loop should run the eight types in parallel and expect most types to quit early on this build.
- The replayer (breakers/replay.py) did not finish 190 actions in 10 minutes; replaying a long session needs a longer budget or replay only up to each claim's n in turn. Noted for the first loop; no claim below is machine-confirmed yet.
- Each shell call of a helper is a fresh shell: the brief must tell it to put LEDGER_PLAY_PORT on every command (added to the launch prompt).

## What the testers found on round 5 (to be confirmed by replay in the first loop)
1. The pause menu cannot be used from the keyboard: arrows, Tab and Enter never move off Carry On, so Save, the keys page and every other item need a mouse. Both testers, independently. Blocks save-and-reload tests by keys.
2. The rusher quit at minute 2.1: under the blue sign at Mickey's the to-do stays "Find Mickey's" and the door gives no prompt unless Tom stands on one exact spot (the breaker found it: "Talk to the woman on the radio"). The arrival is not recognised and the next aim never appears.
3. Typed sums in talk ("pay me 500 pounds") are logged as Tom trying to put money in Pauline's hand, with no money moving; the Ledger line names Pauline twice ("Pauline Kitching knows that you tried to put money in Pauline Kitching's hand").
4. A subtitle line (Ron's) stays on screen for minutes of game time until the next talk.
5. Prompts are drawn over the subtitles.
6. The camera inside Laverack's awning (a grey slab), near the known camera-blocked places of the machine checks.
7. A passer-by walks into Tom and overlaps him.
8. A black frame after closing the pause menu, gone on the next action.
9. The pause menu shows playtest and design entries to a player (known: the prototype's test menu).
10. Needs a look, content rule: Darren's line "I owe the book a few quid" means Mickey's debt book, but "the book" reads as a bookmaker to a British ear. Rewording is the next loop's call (scenes.js line 174).
Held, also unconfirmed by replay: no money from nothing in 4.8 minutes (pocket 23.50 throughout); no paid fare was reached, so fare and save tricks were not tried.

Best moment named: fronting up a passer-by (Q, the ladder of stare, square up, threaten), minute 1.4.

Sessions kept outside the repository (scratch); this note is the record.

Review: a fresh Opus reviewer, PASS WITH FIXES (6 items), all fixed once: design codes stripped from player cards in the brief, no file named in the answer shape, each breaker shown its own type, a dead line removed from launch.py, and this note's two wording points.
