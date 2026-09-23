# The small-model test: the intent router on Qwen3-4B-Instruct-2507, the 42, nofence

42 lines (set: 42), temperature 0, the shipped prompt and validator, small-model wording: nofence. Written by ledger/RouterFloor on 2026-09-23 20:42.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 36/42 (86%) | 5 (12%) | 1 | 0 | 350 | 770 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 4 | 1 |
| oblique verb | 5 | 4 | 1 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 0 | 2 |
| argument | 10 | 9 | 1 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | speech | `{"kind":"speech","why":"buy something nice and keep quiet"}` |
| A | I'll stand everyone in here a drink. | novel | speech | `{"kind":"speech","why":"offer drink to group"}` |
| A | I slip the barman a tenner to tell me who's been asking about me. | novel | pay_off | `{"kind":"verb","verb":"pay_off","args":{},"check":"cash","amount":10,"effect":"suspicion_down","magnitude":0.1,"target":"Rocco","why":"pay t...` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | `{"kind":"speech","why":"be careful who you talk to"}` |
| B | I'm off. Night. | leave | speech | `{"kind":"speech","why":"going to leave the pub"}` |
| C | I'll buy the next round for the whole bar. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing","args":{},"check":"cash","amount":10,"effect":"attention_up","magnitude":0.1,"target":"Sam","why":"to boost...` |
