# The small-model test: the intent router on Gemma 4 E4B it Q4_K_M, 42, nofence+novelok+leavehint

42 lines (set: 42), temperature 0, the shipped prompt and validator, small-model wording: nofence + novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 22:06.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 31/42 (74%) | 2 (5%) | 12 | 3 | 2868 | 3764 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 2 | 0 |
| oblique verb | 5 | 2 | 1 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 0 | 1 |
| argument | 10 | 8 | 0 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Here's a hundred and twenty quid. We never had this conversation. | pay_off | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "pay_off",   "args": {},   "check": "cash",   "amount": 120,   "effect": "` |
| A | That eighty quid you owe me. I'll have it now. | collect_debt | REJECTED:unparseable | `{"kind":"verb","verb":"collect_debt","args":{},"check":"standing","amount":80,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why"...` |
| A | Keep talking about me and you'll be eating through a straw. | lean_on | REJECTED:unparseable | `` |
| A | How much would it take for you to forget you ever heard my name? | pay_off | REJECTED:unparseable | `{"kind":"verb","verb":"pay_off","args":{},"check":"cash","amount":120,"effect":"` |
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | speech | `{"kind":"speech","verb":"<id>","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Rocco","why":"Giving advice ...` |
| A | Spring was a long time ago. You know what you owe. | collect_debt | REJECTED:unparseable | `` |
| A | I'll stand everyone in here a drink. | novel | speech | `{"kind":"speech","verb":"N/A","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Rocco","why":"Offering drinks...` |
| A | I slip the barman a tenner to tell me who's been asking about me. | novel | REJECTED:unparseable | `` |
| B | I'm not leaving till you tell me about the fire. | ask_about(the fire) | REJECTED:unparseable | `` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | REJECTED:unparseable | `` |
| C | I'll buy the next round for the whole bar. | novel | REJECTED:unparseable | `` |
