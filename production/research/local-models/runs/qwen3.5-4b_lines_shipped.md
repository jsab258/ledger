# The small-model test: the intent router on Qwen3.5-4B Q4_K_M, thinking off, lines, shipped

299 lines (set: heldout), temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 21:12.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 235/299 (79%) | 58 (19%) | 8 | 2 | 846 | 1581 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 138 | 1 |
| verb's words, not the verb | 25 | 19 | 6 |
| oblique verb | 59 | 40 | 18 |
| plain verb | 25 | 24 | 0 |
| argument | 16 | 14 | 2 |
| novel | 35 | 0 | 31 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"complimenting hi...` |
| M01 | Give me the keys, I'll do the early airport run myself. | novel | set_cut(fair) | `{"kind":"verb","verb":"set_cut","args":{"policy":"fair"},"check":"crew","amount":0,"effect":"nothing","magnitude":0.05,"target":"Rocco","why...` |
| M02 | Funny, I heard the van's owner lit it himself for the insurance. Mention that to your customers, eh? | plant_doubt | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player is making ...` |
| M02 | Here, give us that crate, I'll carry it out to your van for you. | novel | lean_on | `{"kind":"verb","verb":"lean_on","args":{},"check":"standing","amount":0,"effect":"standing_down","magnitude":0.05,"target":"Rocco","why":"of...` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | collect_debt | `{"kind":"verb","verb":"collect_debt","args":{},"check":"standing","amount":60,"effect":"nothing","magnitude":0.05,"target":"Lena","why":"ask...` |
| M04 | Right, I'm getting out of this rain. Mind how you go. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player is leaving...` |
| M04 | Give us your keys, I'll swap that wiper blade for you now. | novel | collect_debt | `{"kind":"verb","verb":"collect_debt","args":{},"check":"standing","amount":45,"effect":"standing_up","magnitude":0.1,"target":"Rocco","why":...` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sam","why":"offering a scarf"}` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"pay-them-off","args":{},"check":"cash","amount":100,"effect":"standing_up","magnitude":0.05,"target":"Ada","why":"I'm...` |
| M06 | Hold still, I'll wedge a matchbox under that wobbly table leg. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing","args":{},"check":"standing","amount":0,"effect":"standing_up","magnitude":0.05,"target":"Ada","why":"playe...` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | use_hook | `{"kind":"verb","verb":"use_hook","args":{},"check":"hook","effect":"suspicion_up","magnitude":0.08,"target":"Sera Kest","why":"threatening w...` |
| M07 | Right, that's me. I'll let you get back to your forms. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player is politel...` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | use_hook | `{"kind":"verb","verb":"use_hook","args":{},"check":"standing","effect":"standing_up","magnitude":0.08,"target":"Sera Kest","why":"offering h...` |
| M08 | Everybody's got a theory about the fire. I'm sick of hearing them. | speech | ask_about(the fire) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fire"},"target":"Rocco","why":"tired of fire rumors"}` |
| M08 | Hold the torch while I get this padlock off the gate. | novel | set_cut(fair) | `{"kind":"verb","verb":"set_cut","args":{"policy":"fair"},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"...` |
| M09 | do you get many in on a weekday | speech | ask_about(the break-in) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the break-in"},"target":"Father Emil","why":"asking about the break-in"}` |
| M09 | Here, let me carry those hymn books in for you. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Father Emil","why":"offering h...` |
| M10 | Mickey used to let debts ride for months, didn't he? Soft touch. | speech | collect_debt | `{"kind":"verb","verb":"collect_debt","args":{},"check":"standing","amount":120,"effect":"standing_up","magnitude":0.12,"target":"Noor","why"...` |
| M10 | Give us that bundle, I'll get your papers onto the rack for you. | novel | collect_debt | `{"kind":"verb","verb":"collect_debt","args":{},"check":"standing","amount":120,"effect":"standing_up","magnitude":0.12,"target":"Rocco","why...` |
| M11 | Here, that lighter's had it. Let me give you a light off mine. | novel | leave | `{"kind":"verb","verb":"leave","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Mara Ellis","why":"player offer...` |
| M12 | Budge over, I'm getting in out of the rain. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"player is ju...` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"player offer...` |
| M13 | Nobody's threatening anybody, Danny. Tell your mates to calm down. | speech | leave | `{"kind":"verb","verb":"leave","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Danny Ro","why":"player is walk...` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Danny Ro","why":"warning crew about rank","check":"crew","amount":0,"effec...` |
| M13 | Right, that's me. Enjoy the view, lads. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Danny Ro","why":"player is jus...` |
| M13 | I chuck him the keys to Mickey's old Granada. Call it a peace offering. | novel | threaten(quiet) | `{"kind":"verb","verb":"threaten","args":{"tone":"quiet"},"target":"Danny Ro","why":"offering keys as a threat","check":"standing","amount":0...` |
| M14 | Everyone keeps going on at me about that lorry. It's doing my head in. | speech | ask_about(the lorry) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the lorry"},"target":"Sam","why":"complaining about the lorry"}` |
| M14 | Let me grab the other end of that crate for you. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"offering help wit...` |
| M15 | I won't ask you about his last week, June. Not today. | speech | leave | `{"kind":"verb","verb":"leave","args":{}}` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"June","why":"polite farewell"}` |
| M15 | Here, I'll carry these boxes down to the van for you. | novel | leave | `{"kind":"verb","verb":"leave","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"June","why":"player offers to h...` |
| M16 | I'll drop the envelopes round to the lads myself on my way home. | novel | set_cut(fair) | `{"kind":"verb","verb":"set_cut","args":{"policy":"fair"},"target":"Rocco","why":"player offers envelopes to crew","magnitude":0.05}` |
| M17 | Here, I'll clear those back tables for you while you're rushed off your feet. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"offering help wit...` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | threaten(quiet) | `{"kind":"verb","verb":"threaten","args":{"tone":"quiet"},"check":"standing","amount":0,"effect":"standing_up","magnitude":0.05,"target":"Ser...` |
| M18 | Right, that's me. Don't get up. | leave | threaten(quiet) | `{"kind":"verb","verb":"threaten","args":{"tone":"quiet"},"check":"standing","amount":0,"effect":"standing_down","magnitude":0.05,"target":"S...` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"check":"standing","amount":0,"effect":"suspicion_up","magnitude":0.12,"target":"Ser...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sera Kest","why":"complaining ...` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"target":"Noor","why":"sowing doubt about the fire"}` |
| M19 | You were down there when the warehouse went up, weren't you? Go on, what was it like? | ask_about(the fire) | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Noor","why":"asking about the ...` |
| M19 | I need a different story going round about that van. Help me plant some doubt. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the van"},"target":"Noor","why":"requesting a counter-story"}` |
| M19 | I'll run these proofs down to the print room for you. | novel | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the council vote"},"target":"Noor","why":"I'll run these proofs down to the print room ...` |
| M20 | Here, let me fix that gate for you, it's hanging off its hinge. | novel | speech | ````json {"kind":"speech","target":"Rocco","why":"offering repair work"} ```` |
| M21 | Here, have my scarf round your neck, you're shivering. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Elias","why":"offering warmth ...` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Elias","why":"offering a ride ...` |
| M22 | I'll let you get home, councillor. Evening. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Aldous Vane","why":"polite far...` |
| M22 | Give me those files, I'll carry them down to your car for you. | novel | use_hook | `{"kind":"verb","verb":"use_hook","args":{},"check":"standing","amount":0,"effect":"standing_up","magnitude":0.05,"target":"Aldous Vane","why...` |
| M23 | Here, let me help you get these boxes into the back of the van. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"offering help wit...` |
| M24 | Pass us the screwdriver, I'll have a go at fixing that aerial. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"player requests ...` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"player is making...` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"buying paint and ...` |
| M26 | Honestly, I'm sick to death of hearing about that fight. | speech | ask_about(the fight) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fight"},"target":"Sam","why":"player wants to know about the fight"}` |
| M26 | You've carried this place, Sam. From now on you keep a bigger share of your fares. | set_cut(generous) | novel/crew/attention_up | `{"kind":"novel","verb":"offer","args":{"policy":"generous"},"check":"crew","amount":10,"effect":"attention_up","magnitude":0.08,"target":"Sa...` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sam","why":"greeting and warni...` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sam","why":"Sam is explaining ...` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sam","why":"Sam offers tea and...` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | plant_doubt | `{"kind":"verb","verb":"plant_doubt","args":{},"check":"none","effect":"nothing","magnitude":0,"target":"Noor","why":"testing if they'll say ...` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player offers umb...` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | `{"kind":"speech","verb":"offer","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Lena","why":"polite gesture a...` |
| M28 | I'll help stack these chairs so June can get off home. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing_up","args":{},"check":"standing","amount":0,"effect":"standing_up","magnitude":0.05,"target":"June","why":"o...` |
| M29 | Nice and quiet now, just you and me. Breathe a word about tonight and you'll wish you hadn't. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Parade Rats lookout","why":"I'm warning you to stay silent"}` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player is checkin...` |
| M30 | That little business with the kiosk takings. I know about it, and I think you'll help me now. | use_hook | inform(Aldous Vane) | `{"kind":"verb","verb":"inform","args":{"who":"Aldous Vane"},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer",...` |
| M30 | Enjoy the rest of the film. I'll see myself out. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"polite exit ...` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"offering a t...` |
