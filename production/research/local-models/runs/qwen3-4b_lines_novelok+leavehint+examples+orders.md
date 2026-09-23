# The small-model test: the intent router on Qwen3-4B-Instruct-2507 Q4_K_M, lines, novelok+leavehint+examples+orders

299 lines (set: heldout), temperature 0, the shipped prompt and validator, small-model wording: novelok + leavehint, 6 worked examples per line from 225. Written by ledger/RouterFloor on 2026-09-23 22:58.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 273/299 (91%) | 24 (8%) | 2 | 0 | 1526 | 2443 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 136 | 3 |
| verb's words, not the verb | 25 | 18 | 7 |
| oblique verb | 59 | 51 | 7 |
| plain verb | 25 | 24 | 0 |
| argument | 16 | 16 | 0 |
| novel | 35 | 28 | 7 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | Cold enough in here to hang meat. | speech | novel/heat/suspicion_up | `{"kind":"novel","check":"heat","amount":10,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"meat hangs in cold rooms"}` |
| M01 | What sort of cut did Mickey used to give you lot, out of interest? | speech | set_cut(fair) | `{"kind":"verb","verb":"set_cut","args":{"policy":"fair"},"target":"Rocco","why":"what cut Mickey used to give"}` |
| M02 | Lovely steady hands for gutting. You'd want to keep them that way, so the van story stops with you. | lean_on | plant_doubt | `{"kind":"verb","verb":"plant_doubt","args":{},"check":"none","amount":0,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"keep...` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | speech | `{"kind":"speech"}` |
| M06 | I still can't find my way round the Hook without a map. | speech | novel/hook/attention_up | `{"kind":"novel","check":"hook","amount":1,"effect":"attention_up","magnitude":0.1,"target":"Ada","why":"need map to find hook"}` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | novel/cash/suspicion_down | `{"kind":"novel","check":"cash","amount":150,"effect":"suspicion_down","magnitude":0.1,"target":"clerk","why":"claim envelope is yours"}` |
| M08 | Who left this skip full of old tyres, any idea? | speech | ask_about(the warehouse) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the warehouse"},"target":"Rocco","why":"who left skip with tyres"}` |
| M08 | Everybody's got a theory about the fire. I'm sick of hearing them. | speech | ask_about(the fire) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fire"},"target":"Rocco","why":"sick of hearing theories"}` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | `{"kind":"speech","why":"what these papers mean"}` |
| M13 | Nobody's threatening anybody, Danny. Tell your mates to calm down. | speech | threaten(quiet) | `{"kind":"verb","verb":"threaten","args":{"tone":"quiet"},"target":"Rocco","why":"calm down quietly"}` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Danny Ro","why":"warn against targeting my crew"}` |
| M14 | Everyone keeps going on at me about that lorry. It's doing my head in. | speech | ask_about(the lorry) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the lorry"},"target":"the market porter","why":"everyone keeps asking about the lorry"}` |
| M15 | I won't ask you about his last week, June. Not today. | speech | ask_about(Mickey's last week) | `{"kind":"verb","verb":"ask_about","args":{"topic":"Mickey's last week"},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | `{"kind":"speech"}` |
| M19 | Everybody in the Hook wants to talk about that fire. I'm sick of hearing about it. | speech | ask_about(the fire) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fire"},"target":"Noor","why":"sick of hearing about fire"}` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"check":"none","amount":0,"effect":"suspicion_up","magnitude":0.1,"target":"...` |
| M19 | I need a different story going round about that van. Help me plant some doubt. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"target":"Noor","why":"plant doubt about the van"}` |
| M22 | Shame if the committee found out where the money for your extension really came from, Aldous. | use_hook | speech | `{"kind":"speech"}` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | `{"kind":"speech","why":"take fare myself and rest"}` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | `{"kind":"speech","why":"buy paint and nails"}` |
| M26 | Honestly, I'm sick to death of hearing about that fight. | speech | ask_about(the fight) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fight"},"target":"Sam","why":"I'm sick of hearing about the fight"}` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | `{"kind":"speech","why":"going home, phone danger"}` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | `{"kind":"speech","why":"you look done in"}` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | plant_doubt | `{"kind":"verb","verb":"plant_doubt","args":{},"check":"none","amount":0,"effect":"suspicion_up","magnitude":0.1,"target":"Noor","why":"they ...` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | `{"kind":"speech"}` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | `{"kind":"speech"}` |
