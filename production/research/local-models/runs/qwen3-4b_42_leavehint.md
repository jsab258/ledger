# The small-model test: the intent router on Qwen3-4B-Instruct-2507, the 42, leavehint

42 lines (set: 42), temperature 0, the shipped prompt and validator, small-model wording: leavehint. Written by ledger/RouterFloor on 2026-09-23 20:43.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 35/42 (83%) | 7 (17%) | 0 | 0 | 460 | 848 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 5 | 0 |
| oblique verb | 5 | 2 | 3 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 1 | 2 |
| argument | 10 | 8 | 2 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | speech | `{"kind":"speech","why":"buy something nice and keep quiet"}` |
| A | It'd be a shame if your van caught fire one night. | lean_on | speech | `{"kind":"speech","why":"a shame if van catches fire"}` |
| A | Spring was a long time ago. You know what you owe. | collect_debt | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"spring was a long tim...` |
| A | I'll stand everyone in here a drink. | novel | speech | `{"kind":"speech","why":"offer drink to everyone"}` |
| B | Forget the fire. What about the warehouse? | ask_about(the warehouse) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"ask about warehouse"}` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | `{"kind":"speech","why":"be careful who you talk to"}` |
| C | I'll buy the next round for the whole bar. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"buying next round for...` |
