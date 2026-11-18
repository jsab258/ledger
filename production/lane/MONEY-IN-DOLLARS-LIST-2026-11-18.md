# Money written in dollars: the list (18 November 2026)

Lane helper, 18 November 2026. Searched game-design/, production/specs/, canon.md and the player-facing text data (game-design/barks.json, bark-names.json, tier2-batch-1.json, production/specs/suggested-lines.json, town-news.json, in-game.json, street-people.json, the cast files, content/dialogue/, content/brands/, ledger/Assets/Resources/router-examples.json and ledger/Assets/StreamingAssets/). Archives left out. Nothing was changed outside this file.

## What settles it

- canon.md says nothing about currency (no pound, dollar or money rule in it).
- The setting ruling does: game-design/roadmap-history.md line 1624, from the 31 July "the city is British" call, says "Currency is £", and setting-britain-2026-07-31.md item 1 says every amount must change from $ to £ and read as plausible sterling.
- The draft style sheet (production/lane/STYLE-SHEET-1990-DRAFT-2026-11-18.md, section 3) says pounds and pence only: "45p" under a pound, "£1.20", "£12", "£12.50" above; in talk "a fiver", "a tenner", "two quid".
- The game code already shows these same numbers with a £ sign (Economy.cs, PurseSetup.cs, EconomySetup.cs, DialogueUI.cs). Sam's £120, the collection round's £60, the protection round's £80, the fencing line's £100 and the squeezed supplier's "asks £{price}" are all in pounds in code. So the design notes keep their numbers and only change the sign; none of them needs a new pound value.

## Counts

- 123 dollar hits in game-design/ and production/specs/ (none in canon.md), counting lines in text files outside archives; 7 more lines hold "$" only as a pattern-matching sign, not money (clip-findings.txt 5, roadmap-history.md 2754, asset-budgets.json 140). Corrected 18 Nov by review: the first count was 118 and missed three table headers and two switch lines.
- 52 are in-game money written in dollars: these should be pounds. 2 of them are player-facing (how-to-play.md, which is marked as the player's instructions for the prototype).
- 4 only describe the old switch away from dollars and need no change.
- 67 are real-world spending (asset packs, voice services, Anthropic key costs). Those prices really are charged in US dollars, so they are listed below as a group with a proposal, not as faults.
- The player-facing line data has no dollar sign, "dollars" or "bucks" anywhere. One American money idea turned up in the town cards: "medical bills" (twice, the design copy and the game copy).
- The simulation and tool code: 6 places where in-game money is named or written in dollars (listed at the end), no change made.

## In-game money written in dollars (should be pounds)

| File | Line | Text now | Proposed | Player-facing |
|---|---|---|---|---|
| game-design/how-to-play.md | 64 | "The till washes $120/day of dirty money" | "The till washes £120 a day of dirty money" | yes |
| game-design/how-to-play.md | 83 | "evening: $40 clean, and something money can't buy" | "evening: £40 clean, and something money can't buy" | yes |
| game-design/empire-roster.md | 16 | pawnshop row: "clean $900 · his marker $250 ... +$60/day clean, washes $80/day" | "clean £900 · his marker £250 ... +£60 a day clean, washes £80 a day" | no |
| game-design/empire-roster.md | 17 | market stall row: "clean $500 ... +$40/day clean, washes $30/day" | "clean £500 ... +£40 a day clean, washes £30 a day" | no |
| game-design/empire-roster.md | 28 | "Collection round, $60/day dirty" | "£60 a day dirty" | no |
| game-design/empire-roster.md | 29 | "Protection round, $80/day dirty" | "£80 a day dirty" | no |
| game-design/empire-roster.md | 38 | "Sam, $120, cash, counted twice" | "Sam, £120" | no |
| game-design/empire-roster.md | 39 | "Joey, $100" | "Joey, £100" | no |
| game-design/empire-roster.md | 40 | "Marla, $150" | "Marla, £150" | no |
| game-design/empire-roster.md | 41 | "Victor, $200, a slice of his gambling marker cleared" | "Victor, £200, a slice of his debt cleared" (gambling also breaks the content rule) | no |
| game-design/empire-roster.md | 42 | "Any live batch resident, $120 default" | "£120 default" | no |
| game-design/empire-roster.md | 51 | "Ladder: slow beer (0.25) -> $40/day" | "-> £40 a day" (the beer also breaks the content rule) | no |
| game-design/empire-roster.md | 65 | "Fencing line ($100/day, risk 0.4)" | "Fencing line (£100 a day, risk 0.4)" | no |
| game-design/empire-roster.md | 68 | "generous (-$15/day, +loyalty" | "generous (-£15 a day, +loyalty" | no |
| game-design/empire-roster.md | 69 | "skim (+$15/day, -loyalty" | "skim (+£15 a day, -loyalty" | no |
| game-design/empire-roster.md | 71 | "Magda's teahouse ($600, +$45/day, washes $40)" | "Magda's teahouse (£600, +£45 a day, washes £40)" | no |
| game-design/empire-roster.md | 72 | "Donna's bakery ($550 or her $150 marker, +$45/day, washes $25)" | "Donna's bakery (£550 or her £150 marker, +£45 a day, washes £25)" | no |
| game-design/empire-roster.md | 88 | "Meridian Parcel courier rounds, $40 clean a" | "£40 clean a" | no |
| game-design/empire-roster.md | 105 | "$50/day tribute" | "£50 a day tribute" | no |
| game-design/counterparty-purses-spec.md | 16 | "Rita owes $180 and Rita" | "Rita owes £180 and Rita" | no |
| game-design/counterparty-purses-spec.md | 17 | "pays $180, in one movement" | "pays £180, in one movement" | no |
| game-design/counterparty-purses-spec.md | 63 | "A $400 debt against a man who turns" | "A £400 debt against a man who turns" | no |
| game-design/counterparty-purses-spec.md | 64 | "over $90 a week" | "over £90 a week" | no |
| game-design/balance-findings-economy.md | 79 | table header: "avg$" | "avg £" | no |
| game-design/balance-findings-economy.md | 16 | table row: Control, end cash "$2279" | "£2279" | no |
| game-design/balance-findings-economy.md | 17 | table row: Aggressive, "$2185" | "£2185" | no |
| game-design/balance-findings-economy.md | 18 | table row: Cautious, "$1866" | "£1866" | no |
| game-design/balance-findings-economy.md | 24 | "Aggressive play earns $1697" | "earns £1697" | no |
| game-design/balance-findings-economy.md | 25 | "ends with $94 less" | "ends with £94 less" | no |
| game-design/balance-findings-economy.md | 51 | "he asks $118 for it now" (a quote of a game line) | "he asks £118 for it now" (the game line already says £) | no |
| game-design/balance-findings-economy.md | 88 | "can afford his $60" | "can afford his £60" | no |
| game-design/balance-findings-economy.md | 94 | "two visits, $180, done" | "two visits, £180, done" | no |
| game-design/balance-findings-economy.md | 95 | "Sam produces $45 against a $120 marker" | "Sam produces £45 against a £120 marker" | no |
| game-design/balance-findings-economy.md | 98 | "Same end cash to the dollar" | "Same end cash to the penny" | no |
| game-design/balance-findings-economy.md | 103 | "aggressive play still earns $1697" | "still earns £1697" | no |
| game-design/balance-findings-economy.md | 104 | "finishes $94 behind" | "finishes £94 behind" | no |
| game-design/balance-findings-open.md | 14 | table header: "racket $" | "racket £" | no |
| game-design/balance-findings-open.md | 16 | table row: Control, "$2825" | "£2825" | no |
| game-design/balance-findings-open.md | 17 | table row: Aggressive, "$3138" and "$1708" | "£3138" and "£1708" | no |
| game-design/balance-findings-open.md | 18 | table row: Cautious, "$2512" and "$469" | "£2512" and "£469" | no |
| game-design/balance-findings-open.md | 23 | "($40/day) plus heat-taxed takings" | "(£40 a day) plus heat-taxed takings" | no |
| game-design/balance-findings-open.md | 27 | "+$313 over control (+11%)" | "+£313 over control (+11%)" | no |
| game-design/balance-findings-open.md | 33 | "The $900 clean purchase hasn't" | "The £900 clean purchase hasn't" | no |
| game-design/balance-findings-open.md | 34 | "amortized by day 21 (+$480 income" | "paid for itself by day 21 (+£480 income" | no |
| game-design/roadmap-history.md | 387 | "aggressive play earns $1697 in racket" | "earns £1697 in racket" | no |
| game-design/roadmap-history.md | 388 | "ends $94 down" | "ends £94 down" | no |
| game-design/roadmap-history.md | 430 | "an introduction and sixty dollars does not silently spend the sixty" | "an introduction and sixty quid does not silently spend the sixty" | no |
| game-design/roadmap-history.md | 482 | "Demands are capped at $800" | "capped at £800" | no |
| game-design/roadmap-history.md | 645 | "Rita owed $180 and produced $180" | "Rita owed £180 and produced £180" | no |
| game-design/roadmap-history.md | 1071 | "reads 346/306/203 dollars" | "reads £346/£306/£203" | no |
| game-design/combat-spec.md | 243 | table header in a code block: "$cost" (the bribe column) | "£cost" | no |
| game-design/production-plan-audio-art.md | 118 | voice test row: "numbers ($120, day 8)" | "numbers (£120, day 8)"; the voice test should read the pound sign, since that is what the game shows | no |

Roadmap-history is a dated history file; changing old entries is a choice for the builder. The other design notes are current and should change.

No "amount to check" marks: every figure above matches the number the game already shows in pounds. One caution from setting-britain item 1 still stands as a design question, not a fault: whether figures like a £900 pawnshop or £120 a day through one pub till read as plausible 1990 sterling. That needs a price check against 1990 sources before any of it reaches a player as a fixed price.

## Mentions of the old switch (no change needed)

| File | Line | Text | Proposed | Player-facing |
|---|---|---|---|---|
| game-design/setting-britain-2026-07-31.md | 29 | table row: magistrate, 5, `$`, economy-wide | none, it lists what the switch changed | no |
| game-design/setting-britain-2026-07-31.md | 77 | "**1. Currency: `$` → `£`.**" | none, it describes the change | no |
| game-design/setting-britain-2026-07-31.md | 79 | "plausible late-analog sterling, not as dollar figures with a different glyph" | none, it describes the change | no |
| game-design/story-outline-2026-09-28.md | 7 | "Where the July drafts assumed a pub, drink or dollars" | none, it describes the change | no |

## Real-world spending in dollars (not game money)

These are real prices charged in US dollars (asset shops, voice services, the Anthropic key), so a pound sign would be wrong. Proposal: write "US$" in current notes so nobody reads them as game money, and add a rough pound figure only where Jafar has to decide on spending. History files can stay as they are.

| File | Lines | Example | Proposed | Player-facing |
|---|---|---|---|---|
| game-design/production-plan-audio-art.md | 37, 38, 40, 42, 97, 444, 445, 446, 447, 455, 461, 582 to 590, 596 to 599, 602, 603, 604, 606, 620 to 627, 631, 633 (38 lines) | "Revised total ~$70 to ~$265" | "US$70 to US$265" | no |
| game-design/shopping-list.md | 27, 35, 60, 61, 77, 111, 114, 136, 142 | "Total: $0." | "US$" throughout | no |
| game-design/the-gap.md | 38, 129, 204 to 207, 209 | "a quarter of a billion dollars" | "US$" for the table; the prose can stay | no |
| game-design/playtest-plan.md | 110, 219 | "under $1"; "well under $10" | "under US$1 (about 80p)" | no |
| game-design/PLAYTEST-RUNBOOK.md | 56 | "measures under a dollar" | "under US$1" | no |
| production/specs/talk-protocol.md | 114, 129 | "dollars at the game's own price table"; "five dollars an evening" | keep "dollars", say "US dollars" | no |
| game-design/m0-plan.md | 66 | "target ≤ $0.05/hr" | "US$0.05 an hour" | no |
| game-design/roadmap-history.md | 219 | "Target < $0.05/hour ambient" | history, leave | no |
| game-design/research-openworld-audit.md | 117, 363 | "per-dollar"; "<$0.05/hour cost envelope" | "per pound spent" or leave; "US$0.05" | no |
| game-design/tier2-pipeline-spec.md | 54 | "low single-digit dollars per 100 cards" | "a few US dollars" | no |
| game-design/voice-casting.md | 54 | "$0, no API" | "free, no API" | no |
| game-design/visual-bar-sources.md | 86 | "one manual click at $0" | "free" | no |
| game-design/research/content-sourcing.md | 208 | "itch.io $0 flows" | "itch.io free downloads" | no |

## Player-facing line data: American money words

| File | Line | Text now | Proposed | Player-facing |
|---|---|---|---|---|
| game-design/tier2-batch-1.json | 2720 | "I owe the pawnshop for my sister's medical bills." | "I owe the pawnshop for my sister's rent arrears." (Britain in 1990 has the NHS; medical bills read as American) | yes, through the town cards |
| ledger/Assets/StreamingAssets/tier2-batch-1.json | 2720 | same line, game copy | same change | yes |

Not money, but found on the way, in player-facing text: how-to-play.md writes "rumors" (line 63) and "company colors" (line 84), and tier2-batch-1.json writes "harbor" (about 50 times), "apartment" and "apartment_steps" (about 20), "favor" and "carburetor". British spelling is harbour, flat, favour, rumours, colours, carburettor. Worth a separate pass; the place name "apartment_steps" is an id and needs care.

## Simulation and tool code (listed only, nothing changed)

In-game money named or written in dollars:

- ledger/Assets/Scripts/Core/IntentRouter.cs lines 122 and 123: comments say the Cash and DirtyCash amounts are "Amount dollars".
- ledger/Assets/Scripts/Core/Access.cs lines 195 and 196: comment, "forty dollars".
- ledger/Assets/Scripts/Core/Empire.cs line 829: comment, "a negative dollar figure".
- ledger/CoreTests/Program.cs line 4240: test message text, "no round ever reports a negative dollar".
- ledger/CoreTests/Program.Part2.cs line 5038: comment, "sixty dollars".
- ledger/SimHarness/Program.cs lines 526, 530, 666 and 740: text the harness sends to the model: "about $120; you have $300", "$80 outstanding", "the bar took $180 yesterday", "the bar took $200 yesterday". These shape test conversations, so they teach the model dollars (and "the bar" for the pub). Line 589 notes this kind of leftover was found once before.
- ledger/BalanceLab/Program.cs line 673: comment, "Returns dollars spent".

Real API spending in dollars (correct as US dollars, listed for completeness): TalkHelper/Program.cs (SpentUsd, CapUsd, "--budget-usd", the "US$" evening message at line 1363), ClaimBench (KeyRuns.cs, FastFirst.cs "measuring dollar", "usd" log field), TalkTests, Core/CostTracker.cs, Core/BudgetedClient.cs, Core/LlmClient.cs, Core/ClaimCheck.cs, Core/ConversationEngine.cs; ledger/sim-report.md lines 160 and 169 ("$0.0315"). Core/MotionMatch.cs line 31 quotes a real price ("$100–1000"). The "cents" in Game/Audio.cs are musical tuning, not money.

## Suggested guard

The style sheet already suggests a word check for "$" in content/. It would have caught the harness leftover too if it also ran over the town cards and the SimHarness prompt strings.
