# The small-model test: the intent router on Qwen3.5-4B Q4_K_M, thinking off, lines, nofence+novelok+leavehint

299 lines (set: heldout), temperature 0, the shipped prompt and validator, small-model wording: nofence + novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 21:18.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 236/299 (79%) | 58 (19%) | 6 | 1 | 764 | 1318 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 136 | 3 |
| verb's words, not the verb | 25 | 19 | 6 |
| oblique verb | 59 | 42 | 16 |
| plain verb | 25 | 24 | 0 |
| argument | 16 | 14 | 2 |
| novel | 35 | 1 | 31 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"Rocco is being t...` |
| M01 | Give me the keys, I'll do the early airport run myself. | novel | set_cut(fair) | `{"kind":"verb","verb":"set_cut","args":{"policy":"fair"},"check":"crew","amount":0,"effect":"nothing","magnitude":0.05,"target":"Rocco","why...` |
| M02 | Funny, I heard the van's owner lit it himself for the insurance. Mention that to your customers, eh? | plant_doubt | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player is making ...` |
| M02 | Here, give us that crate, I'll carry it out to your van for you. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player offers cra...` |
| M03 | Tear out your page. Mickey would've wanted it, and so do I. | forgive_debt | novel/standing/nothing | `{"kind":"novel","verb":"burn_ledger","args":{},"check":"standing","amount":0,"effect":"nothing","magnitude":0.05,"target":"Lena","why":"burn...` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | collect_debt | `{"kind":"verb","verb":"collect_debt","args":{},"check":"standing","amount":60,"effect":"nothing","magnitude":0.05,"target":"Lena","why":"ask...` |
| M04 | Mickey never walked away from a driver in trouble, did he? | speech | lean_on | `{"kind":"verb","verb":"lean_on","args":{},"check":"standing","amount":0,"effect":"suspicion_up","magnitude":0.08,"target":"Rocco","why":"hin...` |
| M04 | Give us your keys, I'll swap that wiper blade for you now. | novel | collect_debt | `{"kind":"verb","verb":"collect_debt","args":{},"check":"cash","amount":45,"effect":"standing","magnitude":0.1,"target":"Rocco","why":"offeri...` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sam","why":"giving a scarf for...` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"pay","args":{},"check":"cash","amount":100,"effect":"standing_up","magnitude":0.05,"target":"Ada","why":"player offer...` |
| M06 | Hold still, I'll wedge a matchbox under that wobbly table leg. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing","args":{},"check":"standing","amount":0,"effect":"standing_up","magnitude":0.05,"target":"Ada","why":"playe...` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | use_hook | `{"kind":"verb","verb":"use_hook","args":{},"check":"hook","effect":"standing_up","magnitude":0.08,"target":"Sera Kest","why":"threatening wi...` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | use_hook | `{"kind":"verb","verb":"use_hook","args":{},"check":"standing","effect":"standing_up","magnitude":0.05,"target":"Sera Kest","why":"offering t...` |
| M08 | The office is skimming yours from now on, Rocco. Take it up with me if you don't like it. | set_cut(skim) | novel/none/nothing | `{"kind":"novel","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"player threatens ...` |
| M08 | Hold the torch while I get this padlock off the gate. | novel | ask_about(the fire) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fire"},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","w...` |
| M09 | do you get many in on a weekday | speech | ask_about(the funeral) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the funeral"},"target":"Father Emil","why":"asking about funeral attendance"}` |
| M09 | I didn't see much at the funeral myself. I was stood right at the back. | speech | ask_about(the funeral) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the funeral"},"target":"Father Emil","why":"player claims they saw nothing at the funeral...` |
| M09 | Here, let me carry those hymn books in for you. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Father Emil","why":"offering h...` |
| M10 | Give us that bundle, I'll get your papers onto the rack for you. | novel | collect_debt | `{"kind":"verb","verb":"collect_debt","args":{},"check":"standing","amount":120,"effect":"standing_up","magnitude":0.12,"target":"Noor","why"...` |
| M11 | Here, that lighter's had it. Let me give you a light off mine. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Mara Ellis","why":"polite offe...` |
| M12 | Budge over, I'm getting in out of the rain. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"player is ju...` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"player offer...` |
| M13 | Your lads always this chatty, Danny? | speech | leave | `{"kind":"verb","verb":"leave","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Danny Ro","why":"player is endi...` |
| M13 | Nobody's threatening anybody, Danny. Tell your mates to calm down. | speech | threaten(quiet) | `{"kind":"verb","verb":"threaten","args":{"tone":"quiet"},"target":"Danny Ro","why":"telling crew to calm down","check":"crew","amount":0,"ef...` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | threaten(loud) | ````json {"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Danny Ro","why":"warns crew about his rank","check":"crew","amount...` |
| M14 | Everyone keeps going on at me about that lorry. It's doing my head in. | speech | ask_about(the lorry) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the lorry"},"target":"Sam","why":"player asks about the lorry"}` |
| M14 | Let me grab the other end of that crate for you. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"offering help wit...` |
| M15 | He never threw a thing away, did he? | speech | ask_about(Mickey's last week) | `{"kind":"verb","verb":"ask_about","args":{"topic":"Mickey's last week"},"target":"June","why":"checking if he kept evidence"}` |
| M15 | I won't ask you about his last week, June. Not today. | speech | leave | `{"kind":"verb","verb":"leave","args":{},"check":"none","amount":0,"effect":"nothing","target":"June","why":"player is ending the conversatio...` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"June","why":"polite farewell"}` |
| M15 | Here, I'll carry these boxes down to the van for you. | novel | leave | `{"kind":"verb","verb":"leave","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"June","why":"player is walking ...` |
| M16 | I'll drop the envelopes round to the lads myself on my way home. | novel | set_cut(fair) | `{"kind":"verb","verb":"set_cut","args":{"policy":"fair"},"target":"Rocco","why":"player offers to handle envelopes themselves"}` |
| M17 | Here, I'll clear those back tables for you while you're rushed off your feet. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"offering help wit...` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | threaten(quiet) | `{"kind":"verb","verb":"threaten","args":{"tone":"quiet"},"target":"Sera Kest","why":"demanding rank with quiet pressure"}` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"check":"standing","amount":0,"effect":"nothing","magnitude":0.05,"target":"Sera Kes...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sera Kest","why":"complaining ...` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"target":"Noor","why":"sowing a rumor about the fire","check":"none","amount...` |
| M19 | You were down there when the warehouse went up, weren't you? Go on, what was it like? | ask_about(the fire) | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Noor","why":"asking about the ...` |
| M19 | I need a different story going round about that van. Help me plant some doubt. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the van"},"target":"Noor","why":"requesting counter-story"}` |
| M19 | I'll run these proofs down to the print room for you. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Noor","why":"offering to help ...` |
| M20 | Mickey's gone, and so's your page in his book. Consider yourself square. | forgive_debt | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player is speakin...` |
| M20 | Here, let me fix that gate for you, it's hanging off its hinge. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player offers rep...` |
| M21 | Here, have my scarf round your neck, you're shivering. | novel | speech | `{"kind":"speech","verb":"comfort","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Elias","why":"offering warm...` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Elias","why":"offering a ride ...` |
| M22 | Give me those files, I'll carry them down to your car for you. | novel | use_hook | `{"kind":"verb","verb":"use_hook","args":{},"check":"standing","amount":0,"effect":"standing_up","magnitude":0.05,"target":"Aldous Vane","why...` |
| M23 | Here, let me help you get these boxes into the back of the van. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"van driver","why":"offering he...` |
| M24 | Pass us the screwdriver, I'll have a go at fixing that aerial. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"player requests ...` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"player is making...` |
| M25 | Whatever you saw Rocco do last week, you didn't see it. Be a pity about all this glass. | lean_on | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"complaining abou...` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"buying paint and ...` |
| M26 | You've carried this place, Sam. From now on you keep a bigger share of your fares. | set_cut(generous) | novel/crew/attention_up | `{"kind":"novel","verb":"offer","args":{"policy":"generous"},"check":"crew","amount":10,"effect":"attention_up","magnitude":0.08,"target":"Sa...` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sam","why":"polite farewell ab...` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sam","why":"offering tea and c...` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Noor","why":"gossip about the ...` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player offers umb...` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | `{"kind":"speech","verb":"offer","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Lena","why":"player offers te...` |
| M28 | I'll help stack these chairs so June can get off home. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing_up","args":{},"check":"standing","amount":0,"effect":"standing_up","magnitude":0.05,"target":"June","why":"h...` |
| M29 | Nice and quiet now, just you and me. Breathe a word about tonight and you'll wish you hadn't. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Parade Rats lookout","why":"I'm warning him to stay silent"}` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"player is checkin...` |
| M30 | Nobody ever informs on anybody in the Hook, do they? Funny place. | speech | inform(Aldous Vane) | `{"kind":"verb","verb":"inform","args":{"who":"Aldous Vane"},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer",...` |
| M30 | That little business with the kiosk takings. I know about it, and I think you'll help me now. | use_hook | inform(Aldous Vane) | `{"kind":"verb","verb":"inform","args":{"who":"Aldous Vane"},"check":"standing","amount":10,"effect":"suspicion_up","magnitude":0.08,"target"...` |
| M30 | Enjoy the rest of the film. I'll see myself out. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"polite exit ...` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"offering a t...` |
