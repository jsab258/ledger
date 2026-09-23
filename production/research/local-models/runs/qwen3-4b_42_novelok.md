# The small-model test: the intent router on Qwen3-4B-Instruct-2507, the 42, novelok

42 lines (set: 42), temperature 0, the shipped prompt and validator, small-model wording: novelok. Written by ledger/RouterFloor on 2026-09-23 20:43.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 33/42 (79%) | 8 (19%) | 1 | 0 | 509 | 784 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 4 | 1 |
| oblique verb | 5 | 2 | 3 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 2 | 0 |
| argument | 10 | 6 | 4 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| A | Buy yourself something nice, and keep the story to yourself. | pay_off | novel/cash/suspicion_down | `{"kind":"novel","check":"cash","amount":150,"effect":"suspicion_down","magnitude":0.1,"target":"Rocco","why":"buy nice and keep quiet"}` |
| A | It'd be a shame if your van caught fire one night. | lean_on | novel/heat/suspicion_up | `{"kind":"novel","check":"heat","amount":10,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"fear of fire danger"}` |
| A | Spring was a long time ago. You know what you owe. | collect_debt | speech | `{"kind":"speech","why":"spring was a long time ago"}` |
| B | Somebody started that fire. Who? | ask_about(the fire) | speech | `{"kind":"speech","why":"who started the fire"}` |
| B | Forget the fire. What about the warehouse? | ask_about(the warehouse) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"ask about warehouse"}` |
| B | Keep your voice down. If you talk, I'll know. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Lena","why":"warn against speaking out"}` |
| B | YOU WANT TO BE VERY CAREFUL WHO YOU TALK TO! | threaten(loud) | speech | `{"kind":"speech","why":"be careful who you talk to"}` |
| B | I'm off. Night. | leave | speech | `{"kind":"speech","why":"going home, night time"}` |
| C | I'll buy the next round for the whole bar. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing","args":{},"check":"cash","amount":1,"effect":"attention_up","magnitude":0.1,"target":"Sam","why":"to share ...` |
