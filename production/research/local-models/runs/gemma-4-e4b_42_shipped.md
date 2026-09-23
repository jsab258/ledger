# The small-model test: the intent router on Gemma 4 E4B it Q4_K_M, 42, shipped

42 lines (set: 42), temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 21:42.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 22/42 (52%) | 0 (0%) | 31 | 11 | 3789 | 5139 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 2 | 0 |
| oblique verb | 5 | 0 | 0 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 0 | 0 |
| argument | 10 | 1 | 0 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Here's a hundred and twenty quid. We never had this conversation. | pay_off | REJECTED:unparseable | `` |
| A | That eighty quid you owe me. I'll have it now. | collect_debt | REJECTED:unparseable | `` |
| A | Keep talking about me and you'll be eating through a straw. | lean_on | REJECTED:unparseable | `` |
| A | How much would it take for you to forget you ever heard my name? | pay_off | REJECTED:unparseable | `` |
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | REJECTED:unparseable | `` |
| A | It'd be a shame if your van caught fire one night. | lean_on | REJECTED:unparseable | `` |
| A | You've owed me since spring, Rocco. | collect_debt | REJECTED:unparseable | `` |
| A | Spring was a long time ago. You know what you owe. | collect_debt | REJECTED:unparseable | `` |
| A | I'll stand everyone in here a drink. | novel | REJECTED:unparseable | `` |
| A | I slip the barman a tenner to tell me who's been asking about me. | novel | REJECTED:unparseable | `` |
| B | Tell me what you saw at the fire. | ask_about(the fire) | REJECTED:unparseable | `` |
| B | Somebody started that fire. Who? | ask_about(the fire) | REJECTED:unparseable | `` |
| B | Forget the fire. What about the warehouse? | ask_about(the warehouse) | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {     "topic": "` |
| B | I'm not leaving till you tell me about the fire. | ask_about(the fire) | REJECTED:unparseable | `` |
| B | Two hundred and forty, and you never saw me. | pay_off(240) | REJECTED:unparseable | `` |
| B | A hundred and twenty says you forget tonight. | pay_off(120) | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "pay` |
| B | Take the two-forty and keep your mouth shut. | pay_off(240) | REJECTED:unparseable | `` |
| B | Keep your voice down. If you talk, I'll know. | threaten(quiet) | REJECTED:unparseable | `` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | REJECTED:unparseable | `` |
| C | I'll buy the next round for the whole bar. | novel | REJECTED:unparseable | `` |
