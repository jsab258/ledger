# The small-model test: the intent router on Qwen3-4B-Instruct-2507 Q4_K_M, lines, examples+orders, IDLE CARD 24 Sep

299 lines (set: heldout), temperature 0, the shipped prompt and validator, 6 worked examples per line from 225. Written by ledger/RouterFloor on 2026-09-24 07:29.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 271/299 (91%) | 26 (9%) | 2 | 0 | 1403 | 2123 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 138 | 1 |
| verb's words, not the verb | 25 | 18 | 7 |
| oblique verb | 59 | 50 | 8 |
| plain verb | 25 | 24 | 0 |
| argument | 16 | 16 | 0 |
| novel | 35 | 25 | 10 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | What sort of cut did Mickey used to give you lot, out of interest? | speech | set_cut(fair) | `{"kind":"verb","verb":"set_cut","args":{"policy":"fair"},"target":"Rocco","why":"what cut Mickey used to give"}` |
| M01 | Right, that's me. Hold the fort. | leave | speech | `{"kind":"speech"}` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | plant_doubt | `{"kind":"verb","verb":"plant_doubt","args":{},"check":"none","amount":0,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"sugg...` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | speech | `{"kind":"speech"}` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"paying bills toda...` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | speech | `{"kind":"speech"}` |
| M08 | Who left this skip full of old tyres, any idea? | speech | ask_about(the warehouse) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the warehouse"},"target":"Rocco","why":"who left skip with tyres"}` |
| M08 | Everybody's got a theory about the fire. I'm sick of hearing them. | speech | ask_about(the fire) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fire"},"target":"Rocco","why":"sick of hearing theories"}` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | `{"kind":"speech","why":"what these papers mean"}` |
| M13 | Nobody's threatening anybody, Danny. Tell your mates to calm down. | speech | threaten(quiet) | `{"kind":"verb","verb":"threaten","args":{"tone":"quiet"},"target":"Rocco","why":"calm down quietly"}` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Rocco","why":"keep crew off my rank"}` |
| M13 | Right, that's me. Enjoy the view, lads. | leave | speech | `{"kind":"speech"}` |
| M14 | Everyone keeps going on at me about that lorry. It's doing my head in. | speech | ask_about(the lorry) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the lorry"},"target":"the market porter","why":"everyone keeps asking about the lorry"}` |
| M18 | Right, that's me. Don't get up. | leave | speech | `{"kind":"speech"}` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | `{"kind":"speech"}` |
| M19 | Everybody in the Hook wants to talk about that fire. I'm sick of hearing about it. | speech | ask_about(the fire) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fire"},"target":"Noor","why":"everyone talks about the fire"}` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"target":"Noor","why":"spread doubt about the fire"}` |
| M19 | I need a different story going round about that van. Help me plant some doubt. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"target":"Noor","why":"plant doubt about the van"}` |
| M22 | Honestly, what I know about council business would fit on the back of a bus ticket. | speech | use_hook | `{"kind":"verb","verb":"use_hook","args":{},"check":"none","amount":0,"effect":"suspicion_up","magnitude":0.1,"target":"Aldous Vane","why":"I...` |
| M22 | Shame if the committee found out where the money for your extension really came from, Aldous. | use_hook | speech | `{"kind":"speech"}` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | `{"kind":"speech","why":"take fare myself"}` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | `{"kind":"speech","why":"buy paint and nails"}` |
| M26 | Honestly, I'm sick to death of hearing about that fight. | speech | ask_about(the fight) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fight"},"target":"Sam","why":"I'm sick of hearing about the fight"}` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | `{"kind":"speech","why":"going home, phone danger"}` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | `{"kind":"speech"}` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | `{"kind":"speech"}` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | `{"kind":"speech","why":"check cut on hand"}` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | `{"kind":"speech"}` |
