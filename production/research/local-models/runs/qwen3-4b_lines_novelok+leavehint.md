# The small-model test: the intent router on Qwen3-4B-Instruct-2507 Q4_K_M, held-out lines, novelok+leavehint

299 lines (set: heldout), temperature 0, the shipped prompt and validator, small-model wording: novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 22:38.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 229/299 (77%) | 62 (21%) | 8 | 0 | 364 | 1567 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 138 | 1 |
| verb's words, not the verb | 25 | 24 | 1 |
| oblique verb | 59 | 25 | 33 |
| plain verb | 25 | 22 | 2 |
| argument | 16 | 9 | 4 |
| novel | 35 | 11 | 21 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | Cold enough in here to hang meat. | speech | novel/standing/suspicion_up | `{"kind":"novel","check":"standing","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"meat-hanging implies risk"}` |
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | speech | `{"kind":"speech","why":"envelope gets fatter"}` |
| M01 | Office takes a bit extra off the top of yours from now on. Quietly, mind. It won't show on the sheet. | set_cut(skim) | REJECTED:check or effect not in vocabulary | `{"kind":"novel","check":"cut","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"quietly reduce cut"}` |
| M01 | Give me the keys, I'll do the early airport run myself. | novel | leave | `{"kind":"verb","verb":"leave","args":{},"target":"Rocco","why":"take early airport run"}` |
| M02 | Lovely steady hands for gutting. You'd want to keep them that way, so the van story stops with you. | lean_on | speech | `{"kind":"speech","why":"keep van story quiet"}` |
| M02 | Funny, I heard the van's owner lit it himself for the insurance. Mention that to your customers, eh? | plant_doubt | REJECTED:check or effect not in vocabulary | `{"kind":"novel","check":"dirty_cash","amount":50,"effect":"plant_doubt","magnitude":0.1,"target":"Rocco","why":"spread false claim about van...` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | speech | `{"kind":"speech","why":"suggests shifting topic"}` |
| M03 | Tear out your page. Mickey would've wanted it, and so do I. | forgive_debt | novel/none/nothing | `{"kind":"novel","check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"no action required"}` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | speech | `{"kind":"speech","why":"lock ledger in safe tonight"}` |
| M04 | Whatever you've been saying about me in the back of that cab, it stops now, or you'll not be driving anything. | lean_on | novel/standing/suspicion_up | `{"kind":"novel","check":"standing","amount":0,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"threaten to expose cab secrets...` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | `{"kind":"speech","why":"gives scarf to warm someone"}` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"pay","args":{},"check":"cash","amount":20,"effect":"nothing","target":"Sam","why":"settle both bills now"}` |
| M07 | Funny how nobody's ever checked your overtime sheets against the gate log. I have. | use_hook | novel/hook/suspicion_up | `{"kind":"novel","check":"hook","amount":0,"effect":"suspicion_up","magnitude":0.1,"target":"Sera Kest","why":"expose overtime discrepancy"}` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | novel/none/nothing | `{"kind":"novel","check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"player suggests alternative topic"}` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | speech | `{"kind":"speech","why":"ask for help with files"}` |
| M08 | The office is skimming yours from now on, Rocco. Take it up with me if you don't like it. | set_cut(skim) | novel/crew/suspicion_up | `{"kind":"novel","check":"crew","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"claiming office skimming"}` |
| M09 | What did you see at the break-in, Father? | ask_about(the break-in) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Father Emil","why":"ask about th...` |
| M09 | You were at the front for Mickey's service. Notice anyone there who shouldn't have been? | ask_about(the funeral) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"noticed someone out o...` |
| M09 | Not the break-in. The funeral. What did you see there? | ask_about(the funeral) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"ask about the funeral...` |
| M09 | Here, let me carry those hymn books in for you. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"carry hymn books in"}` |
| M10 | Eighty quid, folded in this Gazette. Take it, and the talk about me stops at your counter. | pay_off | novel/cash/standing_down | `{"kind":"novel","check":"cash","amount":80,"effect":"standing_down","magnitude":0.1,"target":"newsagent","why":"stop spreading talk about me...` |
| M10 | Lot of glass in this shop front. You'll want to stop discussing me with your customers. | lean_on | speech | `{"kind":"speech","why":"stop discussing me with customers"}` |
| M10 | Give us that bundle, I'll get your papers onto the rack for you. | novel | speech | `{"kind":"speech","why":"get papers on rack"}` |
| M11 | You might want to look at what comes off Sera Kest's boats after midnight. That's all I'm saying. | inform(Sera Kest) | novel/standing/suspicion_up | `{"kind":"novel","check":"standing","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Sera Kest","why":"report boats after midnigh...` |
| M11 | Not Kest, not Vane. It's Danny Ro you want for the break-in. You didn't get it from me. | inform(Danny Ro) | speech | `{"kind":"speech","why":"point to Danny Ro"}` |
| M12 | Budge over, I'm getting in out of the rain. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why":"move to share s...` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | `{"kind":"speech","why":"what old papers mean"}` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"check":"crew","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","...` |
| M14 | There's a fifty in it for you if last night slips your mind. | pay_off(50) | novel/cash/suspicion_down | `{"kind":"novel","check":"cash","amount":50,"effect":"suspicion_down","magnitude":0.1,"target":"the porter","why":"offer to pay for silence"}` |
| M15 | Was he himself, those last few days before it happened? | ask_about(Mickey's last week) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"none"}` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"nothing to do"}` |
| M16 | Take a bit off the top of every envelope before they go out. The book needs it more than they do. | set_cut(skim) | novel/cash/suspicion_up | `{"kind":"novel","check":"cash","amount":5,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"cut envelopes for book"}` |
| M16 | I'll drop the envelopes round to the lads myself on my way home. | novel | speech | `{"kind":"speech","why":"deliver envelopes to crew"}` |
| M17 | Funny, I heard it was one of Kest's lot that did that van, not me. Pass it on. | plant_doubt | novel/dirty_cash/suspicion_down | `{"kind":"novel","check":"dirty_cash","amount":60,"effect":"suspicion_down","magnitude":0.1,"target":"Ada","why":"discredit Kest's involvemen...` |
| M17 | Put this towards a new urn, and maybe let that story about me go cold. | pay_off | novel/dirty_cash/suspicion_down | `{"kind":"novel","check":"dirty_cash","amount":30,"effect":"suspicion_down","magnitude":0.1,"why":"spread a cold story"}` |
| M17 | You know who really had it in for that van's owner? His own brother-in-law. Worth mentioning to the queue. | plant_doubt | novel/standing/suspicion_up | `{"kind":"novel","check":"standing","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Ada","why":"brother-in-law had it in for van...` |
| M17 | Here, I'll clear those back tables for you while you're rushed off your feet. | novel | speech | `{"kind":"speech","why":"clear tables while busy"}` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | speech | `{"kind":"speech","why":"talk about boat incident"}` |
| M18 | I know your secret, and I'm going to use it against you. | use_hook | novel/hook/suspicion_up | `{"kind":"novel","check":"hook","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Sera Kest","why":"I know your secret"}` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | REJECTED:missing argument | `{"kind":"verb","verb":"threaten","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sera Kest","why":"lay finger...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | `{"kind":"speech","why":"heater is freezing in here"}` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | novel/dirty_cash/suspicion_up | `{"kind":"novel","check":"dirty_cash","amount":50,"effect":"suspicion_up","magnitude":0.1,"target":"Noor","why":"spread doubt about van"}` |
| M19 | You were down there when the warehouse went up, weren't you? Go on, what was it like? | ask_about(the fire) | speech | `{"kind":"speech","why":"recall what was like"}` |
| M19 | I need a different story going round about that van. Help me plant some doubt. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Noor"...` |
| M19 | I'll run these proofs down to the print room for you. | novel | speech | `{"kind":"speech","why":"handing over proofs to print room"}` |
| M20 | Mickey's gone, and so's your page in his book. Consider yourself square. | forgive_debt | speech | `{"kind":"speech","why":"Mickey gone, page removed"}` |
| M21 | Here, have my scarf round your neck, you're shivering. | novel | speech | `{"kind":"speech","why":"offering warmth to Elias"}` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | speech | `{"kind":"speech","why":"offering to drive home"}` |
| M22 | Shame if the committee found out where the money for your extension really came from, Aldous. | use_hook | novel/dirty_cash/suspicion_up | `{"kind":"novel","check":"dirty_cash","amount":5000,"effect":"suspicion_up","magnitude":0.12,"target":"Aldous Vane","why":"expose money sourc...` |
| M22 | I've read the letters from the harbour contractor, Mr Vane. I think you'll vote the way I ask. | use_hook | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"none"}` |
| M22 | I'll let you get home, councillor. Evening. | leave | speech | `{"kind":"speech","why":"evening closing remark"}` |
| M23 | Just between you and me, nice and quiet: one more word about what you saw and you'll regret it. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"van driver","why":"warns of consequences"}` |
| M23 | Here, let me help you get these boxes into the back of the van. | novel | ask_about(the crates) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the crates"},"target":"van driver","why":"help move boxes into van"}` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | `{"kind":"speech","why":"take fare myself"}` |
| M25 | Lena tells me there's a small matter of seventy-five outstanding. Shall we settle it now? | collect_debt | speech | `{"kind":"speech","why":"settle debt with Lena"}` |
| M25 | Whatever you saw Rocco do last week, you didn't see it. Be a pity about all this glass. | lean_on | novel/standing/suspicion_up | `{"kind":"novel","check":"standing","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"blame hidden act"}` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | `{"kind":"speech","why":"buy paint and nails"}` |
| M26 | Honestly, I'm sick to death of hearing about that fight. | speech | ask_about(the fight) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fight"},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sam","wh...` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | `{"kind":"speech","why":"going home, phone danger"}` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | REJECTED:check or effect not in vocabulary | `{"kind":"novel","check":"fair","amount":1,"effect":"suspicion_up","magnitude":0.05,"target":"Sam","why":"fare cut noticed"}` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | `{"kind":"speech","why":"offering comfort to Sam"}` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | novel/none/nothing | `{"kind":"novel","check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"wishing they hadn't spoken"}` |
| M27 | Funny, I heard it wasn't Rocco at all that night. Word is he was across town the whole time. | plant_doubt | novel/none/nothing | `{"kind":"novel","check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"doubt about Rocco's alibi"}` |
| M27 | between us, the story going round has it backwards. ask yourself who gains from blaming Rocco | plant_doubt | speech | `{"kind":"speech","why":"story has it backwards"}` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | `{"kind":"speech","why":"offering umbrella to someone"}` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | `{"kind":"speech","why":"offer tea and cake to Lena"}` |
| M28 | I'll help stack these chairs so June can get off home. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"June","why":"help with chair...` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | `{"kind":"speech","why":"check hand wound"}` |
| M30 | That little business with the kiosk takings. I know about it, and I think you'll help me now. | use_hook | novel/dirty_cash/suspicion_up | `{"kind":"novel","check":"dirty_cash","amount":50,"effect":"suspicion_up","magnitude":0.1,"target":"Aldous Vane","why":"I know about the kios...` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | `{"kind":"speech","why":"offering a snack to the Fixer"}` |
