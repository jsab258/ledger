# The small-model test: the intent router on Qwen3-1.7B Q4_K_M, thinking off, 42, nofence+novelok+leavehint

42 lines (set: 42), temperature 0, the shipped prompt and validator, small-model wording: nofence + novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 22:28.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 22/42 (52%) | 13 (31%) | 7 | 0 | 368 | 443 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 2 | 1 |
| oblique verb | 5 | 0 | 3 |
| talk | 12 | 11 | 1 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 0 | 0 |
| argument | 10 | 2 | 8 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Here's a hundred and twenty quid. We never had this conversation. | pay_off | REJECTED:check or effect not in vocabulary | `</think>  {"kind":"novel","verb":"collect_debt","args":{"amount":80},"check":"none","amount":80,"effect":"dirty_cash","magnitude":0.15,"targ...` |
| A | That eighty quid you owe me. I'll have it now. | collect_debt | REJECTED:unknown argument | `</think>  {"kind":"verb","verb":"collect_debt","args":{"amount":80},"check":"none","amount":80,"effect":"debt","magnitude":0.15,"target":"Le...` |
| A | Keep talking about me and you'll be eating through a straw. | lean_on | speech | `</think>  {"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"Rocco","why":"ask ...` |
| A | How much would it take for you to forget you ever heard my name? | pay_off | REJECTED:unknown argument | `</think>  {"kind":"verb","verb":"pay_off","args":{"amount":120},"check":"none","amount":120,"effect":"standing_up","magnitude":0.15,"target"...` |
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | speech | `</think>  {"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"Rocco","why":"buy ...` |
| A | It'd be a shame if your van caught fire one night. | lean_on | REJECTED:unknown argument | `</think>  {"kind":"verb","verb":"lean_on","args":{"target":"Rocco"},"check":"none","amount":0,"effect":"attention_down","magnitude":0.0,"tar...` |
| A | You've owed me since spring, Rocco. | collect_debt | speech | `</think>  {"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"Rocco","why":"owe ...` |
| A | Spring was a long time ago. You know what you owe. | collect_debt | novel/none/rumor | `</think>  {"kind":"novel","verb":"collect_debt","args":{"amount":80},"check":"none","amount":80,"effect":"rumor","magnitude":0.15,"target":"...` |
| A | I'll stand everyone in here a drink. | novel | REJECTED:unknown argument | `</think>  {"kind":"verb","verb":"lean_on","args":{"target":"Rocco"},"check":"standing","amount":120,"effect":"suspicion_up","magnitude":0.15...` |
| A | I slip the barman a tenner to tell me who's been asking about me. | novel | REJECTED:unknown argument | `</think>  {"kind":"verb","verb":"lean_on","args":{"target":"Rocco"},"check":"none","amount":0,"effect":"attention_down","magnitude":0.0,"tar...` |
| B | Tell me what you saw at the fire. | ask_about(the fire) | speech | `</think>  {"kind":"speech","verb":"ask_about","args":{"topic":"the fire"},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target...` |
| B | Were you anywhere near the warehouse on Tuesday? | ask_about(the warehouse) | speech | `</think>  {"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"Lena","why":"ask a...` |
| B | Somebody started that fire. Who? | ask_about(the fire) | speech | `</think>  {"kind":"speech","verb":"speech","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Lena","why":"ask w...` |
| B | I'm not leaving till you tell me about the fire. | ask_about(the fire) | speech | `</think>  {"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Lena","why":"request...` |
| B | Two hundred and forty, and you never saw me. | pay_off(240) | novel/none/standing_up | `</think>  {"kind":"novel","verb":"pay_off","args":{"amount":240},"check":"none","amount":240,"effect":"standing_up","magnitude":0.15,"target...` |
| B | A hundred and twenty says you forget tonight. | pay_off(120) | novel/none/standing_up | `</think>  {"kind":"novel","verb":"pay_off","args":{"amount":120},"check":"none","amount":120,"effect":"standing_up","magnitude":0.15,"target...` |
| B | Keep your voice down. If you talk, I'll know. | threaten(quiet) | speech | `</think>  {"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"Lena","why":"keep ...` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | `</think>  {"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"Lena","why":"warn ...` |
| B | What was Mickey like, really? | speech | novel/none/rumor | `</think>  {"kind":"novel","verb":"ask_about","args":{"topic":"the fire"},"check":"none","amount":0,"effect":"rumor","magnitude":0.05,"target...` |
| C | I'll buy the next round for the whole bar. | novel | REJECTED:verb not offered | `</think>  {"kind":"verb","verb":"buy","args":{"for":"whole bar"},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"Sam"...` |
