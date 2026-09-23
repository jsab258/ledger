# The small-model test: the intent router on Ministral 3 3B Instruct 2512 Q4_K_M, the 42, nofence+novelok+leavehint

42 lines (set: 42), temperature 0, the shipped prompt and validator, small-model wording: nofence + novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 20:47.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 36/42 (86%) | 5 (12%) | 1 | 0 | 921 | 1247 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 4 | 1 |
| oblique verb | 5 | 3 | 2 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 1 | 1 |
| argument | 10 | 9 | 1 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Here's a hundred and twenty quid. We never had this conversation. | pay_off | novel/dirty_cash/standing_down | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 120,   "effect": "standing_down",   "magnitude": 0.10,   "target": "Rocco"...` |
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 100,   "effect": "suspicion_up",   "magnitude": 0.10,   "target": "Rocco",...` |
| A | It'd be a shame if your van caught fire one night. | lean_on | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Rocco", ...` |
| A | I'll stand everyone in here a drink. | novel | speech | ````json {   "kind": "speech",   "target": "Rocco",   "why": "social_gesture" } ```` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | ````json {   "kind": "speech",   "target": "Lena",   "why": "warn cautious" } ```` |
| C | I'll buy the next round for the whole bar. | novel | REJECTED:verb not offered | ````json {   "kind": "verb",   "verb": "cash",   "check": "cash",   "amount": 50,   "effect": "nothing",   "magnitude": 0.15,   "target": "ba...` |
