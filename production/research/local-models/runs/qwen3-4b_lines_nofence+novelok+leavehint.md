# The small-model test: the intent router on Qwen3-4B-Instruct-2507 Q4_K_M, lines, nofence+novelok+leavehint

299 lines (set: heldout), temperature 0, the shipped prompt and validator, small-model wording: nofence + novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 21:05.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 242/299 (81%) | 50 (17%) | 7 | 0 | 438 | 1125 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 139 | 0 |
| verb's words, not the verb | 25 | 22 | 3 |
| oblique verb | 59 | 34 | 24 |
| plain verb | 25 | 22 | 2 |
| argument | 16 | 9 | 5 |
| novel | 35 | 16 | 16 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | What sort of cut did Mickey used to give you lot, out of interest? | speech | set_cut(fair) | `{"kind":"verb","verb":"set_cut","args":{"policy":"fair"},"target":"Rocco","why":"ask about past cut policy"}` |
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | speech | `{"kind":"speech","why":"envelope gets fatter"}` |
| M01 | Office takes a bit extra off the top of yours from now on. Quietly, mind. It won't show on the sheet. | set_cut(skim) | novel/dirty_cash/suspicion_up | `{"kind":"novel","check":"dirty_cash","amount":10,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"quietly take extra cut"}` |
| M01 | Give me the keys, I'll do the early airport run myself. | novel | leave | `{"kind":"verb","verb":"leave","args":{},"target":"Rocco","why":"take early airport run"}` |
| M02 | Funny, I heard the van's owner lit it himself for the insurance. Mention that to your customers, eh? | plant_doubt | novel/dirty_cash/rumor | `{"kind":"novel","check":"dirty_cash","amount":50,"effect":"rumor","magnitude":0.12,"target":"Rocco","why":"spread false claim to customers"}` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | novel/none/nothing | `{"kind":"novel","check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"no action taken"}` |
| M03 | Tear out your page. Mickey would've wanted it, and so do I. | forgive_debt | novel/none/nothing | `{"kind":"novel","check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"request to tear out page"}` |
| M05 | Time somebody put Danny Ro's name in front of the law. I'll see to it tonight. | inform(Danny Ro) | novel/dirty_cash/suspicion_up | `{"kind":"novel","check":"dirty_cash","amount":500,"effect":"suspicion_up","magnitude":0.1,"target":"Danny Ro","why":"ensure his name is expo...` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"give scarf to Sam"}` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"pay","args":{},"check":"cash","amount":20,"effect":"nothing","magnitude":0.05,"target":"Sam","why":"paying for both b...` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | speech | `{"kind":"speech","why":"envelope belongs to you"}` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | speech | `{"kind":"speech","why":"offering to help carry files"}` |
| M08 | The office is skimming yours from now on, Rocco. Take it up with me if you don't like it. | set_cut(skim) | novel/crew/suspicion_up | `{"kind":"novel","check":"crew","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"threaten crew skimming"}` |
| M09 | What did you see at the break-in, Father? | ask_about(the break-in) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"ask about the break-i...` |
| M09 | You were at the front for Mickey's service. Notice anyone there who shouldn't have been? | ask_about(the funeral) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"noticed someone out o...` |
| M09 | Not the break-in. The funeral. What did you see there? | ask_about(the funeral) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"ask about the funeral...` |
| M10 | Eighty quid, folded in this Gazette. Take it, and the talk about me stops at your counter. | pay_off | novel/cash/standing_down | `{"kind":"novel","check":"cash","amount":80,"effect":"standing_down","magnitude":0.1,"target":"newsagent","why":"pay to stop talk"}` |
| M10 | Lot of glass in this shop front. You'll want to stop discussing me with your customers. | lean_on | novel/standing/attention_down | `{"kind":"novel","check":"standing","amount":0,"effect":"attention_down","magnitude":0.1,"target":"newsagent","why":"stop discussing me with ...` |
| M10 | Give us that bundle, I'll get your papers onto the rack for you. | novel | speech | `{"kind":"speech","why":"get papers on rack for you"}` |
| M11 | You might want to look at what comes off Sera Kest's boats after midnight. That's all I'm saying. | inform(Sera Kest) | novel/standing/suspicion_up | `{"kind":"novel","check":"standing","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Sera Kest","why":"check boats after midnight...` |
| M11 | Not Kest, not Vane. It's Danny Ro you want for the break-in. You didn't get it from me. | inform(Danny Ro) | speech | `{"kind":"speech","why":"point to Danny Ro for break-in"}` |
| M12 | Budge over, I'm getting in out of the rain. | novel | speech | `{"kind":"speech","why":"getting in out of the rain"}` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | `{"kind":"speech","why":"passing papers to ask meaning"}` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"check":"crew","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","...` |
| M15 | I won't ask you about his last week, June. Not today. | speech | leave | `{"kind":"verb","verb":"leave","args":{}, "check":"none", "amount":0, "effect":"nothing", "magnitude":0.0, "target":"June", "why":"I won't as...` |
| M15 | Was he himself, those last few days before it happened? | ask_about(Mickey's last week) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"ask about Mickey's la...` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"goodbye and care"}` |
| M16 | Take a bit off the top of every envelope before they go out. The book needs it more than they do. | set_cut(skim) | REJECTED:check or effect not in vocabulary | `{"kind":"novel","check":"skim","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Lena","why":"cut envelopes for book"}` |
| M17 | Put this towards a new urn, and maybe let that story about me go cold. | pay_off | novel/dirty_cash/suspicion_down | `{"kind":"novel","check":"dirty_cash","amount":100,"effect":"suspicion_down","magnitude":0.1,"why":"plant a false story"}` |
| M17 | You know who really had it in for that van's owner? His own brother-in-law. Worth mentioning to the queue. | plant_doubt | speech | `{"kind":"speech","why":"who had it in for van's owner"}` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | speech | `{"kind":"speech","why":"talk about Thursday boat rank"}` |
| M18 | I know your secret, and I'm going to use it against you. | use_hook | novel/hook/suspicion_up | `{"kind":"novel","check":"hook","amount":1,"effect":"suspicion_up","magnitude":0.12,"target":"Sera Kest","why":"I know your secret"}` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | REJECTED:missing argument | `{"kind":"verb","verb":"threaten","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Sera Kest","why":"lay fing...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | `{"kind":"speech","why":"heater is freezing in room"}` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"check":"none","amount":0,"effect":"suspicion_up","magnitude":0.1,"target":"...` |
| M19 | I need a different story going round about that van. Help me plant some doubt. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"check":"none","amount":0,"effect":"suspicion_up","magnitude":0.1,"target":"...` |
| M19 | I'll run these proofs down to the print room for you. | novel | speech | `{"kind":"speech","why":"I'll run these proofs down"}` |
| M20 | Mickey's gone, and so's your page in his book. Consider yourself square. | forgive_debt | speech | `{"kind":"speech","why":"Mickey gone, page removed"}` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | speech | `{"kind":"speech","why":"offering to drive home"}` |
| M22 | Shame if the committee found out where the money for your extension really came from, Aldous. | use_hook | novel/dirty_cash/suspicion_up | `{"kind":"novel","check":"dirty_cash","amount":5000,"effect":"suspicion_up","magnitude":0.12,"target":"Aldous Vane","why":"shame if committee...` |
| M22 | I've read the letters from the harbour contractor, Mr Vane. I think you'll vote the way I ask. | use_hook | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"none"}` |
| M22 | I'll let you get home, councillor. Evening. | leave | speech | `{"kind":"speech","why":"let you get home evening"}` |
| M23 | Here, let me help you get these boxes into the back of the van. | novel | ask_about(the crates) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the crates"},"target":"van driver","why":"help move boxes to van"}` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"take","args":{},"check":"standing","amount":0,"effect":"standing_up","magnitude":0.1,"target":"Rocco","why":"I'll tak...` |
| M25 | Whatever you saw Rocco do last week, you didn't see it. Be a pity about all this glass. | lean_on | novel/standing/suspicion_up | `{"kind":"novel","check":"standing","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"pity about broken glass"}` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | `{"kind":"speech","why":"buy paint and nails"}` |
| M26 | Honestly, I'm sick to death of hearing about that fight. | speech | ask_about(the fight) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fight"},"target":"Sam","why":"I'm tired of hearing about the fight"}` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | `{"kind":"speech","why":"going home, phone danger"}` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | speech | `{"kind":"speech","why":"office cuts fares now"}` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | `{"kind":"speech","why":"offering comfort to Sam"}` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | speech | `{"kind":"speech","why":"many talk and regret it"}` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | `{"kind":"speech","why":"offering umbrella to person"}` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"offer tea and cake"}` |
| M28 | I'll help stack these chairs so June can get off home. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing","args":{},"check":"standing","amount":0,"effect":"attention_up","magnitude":0.1,"target":"June","why":"I'll...` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | `{"kind":"speech","why":"check hand wound"}` |
| M30 | That little business with the kiosk takings. I know about it, and I think you'll help me now. | use_hook | novel/dirty_cash/suspicion_up | `{"kind":"novel","check":"dirty_cash","amount":50,"effect":"suspicion_up","magnitude":0.1,"target":"Aldous Vane","why":"I know about the kios...` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | `{"kind":"speech","why":"offering a snack to the Fixer"}` |
