# Red team briefs (round 1, used unchanged for later rounds unless a catch rate falls under 9 of 10)

Both helpers: fresh Opus, told to read only the copy, no other file, no web.

## A (open-world director)

You are a senior open-world game director reviewing a game description for completeness. The description is the full design of LEDGER, a single-player, third-person PC open-world crime RPG set in a British port town in 1990, aiming at the bar of Kingdom Come: Deliverance II, GTA V and Red Dead Redemption 2 (a small dense town, not a huge map; guns rare; no meters, minimap or stats are deliberate choices, not gaps). A team will build the whole game from this description alone, so anything not defined here will be missing or guessed. List everything a AAA open-world crime game at that bar must have that this description lacks or leaves undefined. Work systematically: the player's moment-to-moment verbs, every system mentioned but never defined, the town and its people, police and law, money and economy over weeks, missions and jobs, story and endings, failure and retry, time, the interface, navigation, saving and menus, settings, controls and accessibility, audio, onboarding, pacing and variety, and anything the reference games' players would expect. Mark each MISSING or UNDEFINED, with why it matters. No Unreal Engine work and no stated exclusions. Numbered lines, ordered by importance.

## B (systems designer, playthrough walk)

You are a lead systems designer who has shipped open-world games. Same game and bar; deliberate choices (one small dense town, rare guns, no meters, minimap or stat numbers, no game over) are not gaps. Method: (1) note every noun or system referred to; (2) check each is specified (rules, numbers, outcomes) and flag those only referred to; (3) walk a whole playthrough hour by hour from launch to credits and after, asking what the player meets that is not defined (getting around, being caught, getting hurt, crashing, losing, selling, saving, quitting, finding the way, passing time, finishing); (4) compare with the categories a professional design document covers. Same output format.

## For the copy

The "LEDGER, as the player plays it" half of the one-shot prompt; part-id tags stripped; the "Ids not placed" note dropped; ten parts' paragraphs removed and recorded in planted.json; from round 2, sections renumbered so no gap shows by numbering.

## Round 2 change (21 Nov 2026, after helper B caught 8 of 10)

B missed the subtitle options and what happens to unacceptable typed input; both are whole categories a design document covers. One sentence added to both briefs (A and B), generic, naming no planted part:

"Also check, one by one, every way the player gives input (keys, pad, mouse, typed text) and what the game does with input it cannot or must not accept, and every option a player expects in Settings and accessibility (text, subtitles, audio, controls, display, comfort)."
