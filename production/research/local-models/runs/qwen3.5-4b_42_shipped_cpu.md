# The small-model test: the intent router on Qwen3.5-4B Q4_K_M, thinking off, 42, shipped_cpu

42 lines (set: 42), temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 21:08.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 37/42 (88%) | 5 (12%) | 0 | 0 | 5102 | 6201 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 5 | 0 |
| oblique verb | 5 | 4 | 1 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 0 | 3 |
| argument | 10 | 9 | 1 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | lean_on | `{"kind":"verb","verb":"lean_on","args":{},"check":"standing","amount":0,"effect":"suspicion_down","magnitude":0.05,"target":"Rocco","why":"a...` |
| A | I'll stand everyone in here a drink. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"offering drinks ...` |
| A | I slip the barman a tenner to tell me who's been asking about me. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"player bribes ba...` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"warning about who...` |
| C | I'll buy the next round for the whole bar. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player offers to ...` |
