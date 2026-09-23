# The small-model test: the intent router on Qwen3-4B-Instruct-2507 Q4_K_M, 42, novelok+leavehint+examples+orders

42 lines (set: 42), temperature 0, the shipped prompt and validator, small-model wording: novelok + leavehint, 6 worked examples per line from 225. Written by ledger/RouterFloor on 2026-09-23 23:07.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 37/42 (88%) | 5 (12%) | 0 | 0 | 2103 | 2964 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 5 | 0 |
| oblique verb | 5 | 4 | 1 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 1 | 2 |
| argument | 10 | 8 | 2 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | lean_on | `{"kind":"verb","verb":"lean_on","args":{},"check":"none","amount":0,"effect":"suspicion_down","magnitude":0.1,"target":"Rocco","why":"buy so...` |
| A | I slip the barman a tenner to tell me who's been asking about me. | novel | pay_off | `{"kind":"verb","verb":"pay_off","args":{},"check":"cash","amount":10,"effect":"suspicion_down","magnitude":0.1,"target":"Rocco","why":"pay t...` |
| B | Keep your voice down. If you talk, I'll know. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Lena","why":"I'll know if you talk"}` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | `{"kind":"speech"}` |
| C | I'll buy the next round for the whole bar. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"buying round for bar"...` |
