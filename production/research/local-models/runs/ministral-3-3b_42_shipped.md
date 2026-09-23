# The small-model test: the intent router on Ministral 3 3B Instruct 2512 Q4_K_M, the 42, shipped

42 lines (set: 42), temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 20:47.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 35/42 (83%) | 6 (14%) | 1 | 0 | 914 | 1101 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 3 | 2 |
| oblique verb | 5 | 4 | 1 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 1 | 1 |
| argument | 10 | 8 | 2 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Here's a hundred and twenty quid. We never had this conversation. | pay_off | novel/dirty_cash/standing_down | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 120,   "effect": "standing_down",   "magnitude": 0.10,   "target": "Rocco"...` |
| A | It'd be a shame if your van caught fire one night. | lean_on | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 100,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Rocco",...` |
| A | I'll stand everyone in here a drink. | novel | speech | ````json {   "kind": "speech",   "target": "Rocco",   "why": "offering hospitality" } ```` |
| B | Keep your voice down. If you talk, I'll know. | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "check": "none",   "effect": "suspicion_up",   "magnitude": ...` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | ````json {   "kind": "speech",   "target": "Lena",   "why": "warning tone" } ```` |
| B | I'm off. Night. | leave | speech | ````json {   "kind": "speech",   "target": "Lena",   "why": "ends conversation politely" } ```` |
| C | I'll buy the next round for the whole bar. | novel | REJECTED:verb not offered | ````json {   "kind": "verb",   "verb": "cash",   "check": "cash",   "amount": 10,   "effect": "nothing",   "magnitude": 0.1,   "target": "bar...` |
