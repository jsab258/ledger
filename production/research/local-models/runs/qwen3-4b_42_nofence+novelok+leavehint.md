# The small-model test: the intent router on Qwen3-4B-Instruct-2507, the 42, nofence+novelok+leavehint

42 lines (set: 42), temperature 0, the shipped prompt and validator, small-model wording: nofence + novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 20:43.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 38/42 (90%) | 3 (7%) | 1 | 0 | 500 | 835 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 5 | 0 |
| oblique verb | 5 | 3 | 2 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 2 | 0 |
| argument | 10 | 9 | 1 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | novel/cash/suspicion_down | `{"kind":"novel","check":"cash","amount":150,"effect":"suspicion_down","magnitude":0.1,"target":"Rocco","why":"buy nice and keep quiet"}` |
| A | It'd be a shame if your van caught fire one night. | lean_on | novel/heat/suspicion_up | `{"kind":"novel","check":"heat","amount":10,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"fear of van fire"}` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | `{"kind":"speech","why":"be careful who you talk to"}` |
| C | I'll buy the next round for the whole bar. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing","args":{},"check":"cash","amount":10,"effect":"attention_up","magnitude":0.1,"target":"Sam","why":"buying t...` |
