# The small-model test: the intent router on Qwen3-4B-Instruct-2507 Q4_K_M, llama.cpp b11111 Vulkan, RX 6700, rerun with the guard, fence and checker fix

42 lines, three moments, temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 20:32.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 32/42 (76%) | 10 (24%) | 0 | 0 | 327 | 785 |
| JSON constrained | 32/42 (76%) | 10 (24%) | 0 | 0 | 387 | 794 |

## By kind of line

| kind | lines | prompt right | json right | prompt well-formed wrong | json well-formed wrong |
|---|---|---|---|---|---|
| plain verb | 5 | 4 | 4 | 1 | 1 |
| oblique verb | 5 | 2 | 2 | 3 | 3 |
| talk | 12 | 12 | 12 | 0 | 0 |
| verb's words, not the verb | 4 | 4 | 4 | 0 | 0 |
| command | 3 | 3 | 3 | 0 | 0 |
| novel | 3 | 1 | 1 | 2 | 2 |
| argument | 10 | 6 | 6 | 4 | 4 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | speech | `{"kind":"speech","why":"buy something nice and keep quiet"}` |
| A | It'd be a shame if your van caught fire one night. | lean_on | speech | `{"kind":"speech","why":"a shame if van catches fire"}` |
| A | Spring was a long time ago. You know what you owe. | collect_debt | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"spring was a long tim...` |
| A | I'll stand everyone in here a drink. | novel | speech | `{"kind":"speech","why":"offer drink to everyone"}` |
| B | Somebody started that fire. Who? | ask_about(the fire) | speech | `{"kind":"speech","why":"who started the fire"}` |
| B | Forget the fire. What about the warehouse? | ask_about(the warehouse) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"ask about warehouse"}` |
| B | Keep your voice down. If you talk, I'll know. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Lena","why":"warn against speaking out"}` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | `{"kind":"speech","why":"be careful who you talk to"}` |
| B | I'm off. Night. | leave | speech | `{"kind":"speech","why":"going home, night"}` |
| C | I'll buy the next round for the whole bar. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"buying next round"}` |

## Every line the json mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | speech | `{"kind":"speech","why":"buy something nice and keep quiet"}` |
| A | It'd be a shame if your van caught fire one night. | lean_on | speech | `{"kind":"speech","why":"a shame if van catches fire"}` |
| A | Spring was a long time ago. You know what you owe. | collect_debt | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"spring was a long tim...` |
| A | I'll stand everyone in here a drink. | novel | speech | `{"kind":"speech","why":"offer drink to everyone"}` |
| B | Somebody started that fire. Who? | ask_about(the fire) | speech | `{"kind":"speech","why":"who started the fire"}` |
| B | Forget the fire. What about the warehouse? | ask_about(the warehouse) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"ask about warehouse"}` |
| B | Keep your voice down. If you talk, I'll know. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Lena","why":"warn against speaking out"}` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | `{"kind":"speech","why":"be careful who you talk to"}` |
| B | I'm off. Night. | leave | speech | `{"kind":"speech","why":"going home, night"}` |
| C | I'll buy the next round for the whole bar. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"buying next round"}` |
