# The small-model test: the intent router on Qwen3-4B-Instruct-2507 Q4_K_M, lines, shipped

299 lines (set: heldout), temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 21:02.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 216/299 (72%) | 78 (26%) | 5 | 0 | 333 | 1068 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 139 | 0 |
| verb's words, not the verb | 25 | 24 | 1 |
| oblique verb | 59 | 18 | 41 |
| plain verb | 25 | 23 | 1 |
| argument | 16 | 9 | 5 |
| novel | 35 | 3 | 30 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | speech | `{"kind":"speech","why":"envelope gets fatter"}` |
| M01 | Right, that's me. Hold the fort. | leave | speech | `{"kind":"speech","why":"hold fort in office"}` |
| M01 | Office takes a bit extra off the top of yours from now on. Quietly, mind. It won't show on the sheet. | set_cut(skim) | REJECTED:check or effect not in vocabulary | `{"kind":"novel","check":"cut","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"quietly reduce cut"}` |
| M01 | Give me the keys, I'll do the early airport run myself. | novel | speech | `{"kind":"speech","why":"take early airport run"}` |
| M02 | Lovely steady hands for gutting. You'd want to keep them that way, so the van story stops with you. | lean_on | speech | `{"kind":"speech","why":"keep van story quiet"}` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | speech | `{"kind":"speech","why":"suggests shifting topic"}` |
| M02 | Here, give us that crate, I'll carry it out to your van for you. | novel | speech | `{"kind":"speech","why":"ask for crate delivery"}` |
| M03 | Tear out your page. Mickey would've wanted it, and so do I. | forgive_debt | speech | `{"kind":"speech","why":"Tear out page for Mickey"}` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | speech | `{"kind":"speech","why":"locking ledger in safe"}` |
| M04 | Whatever you've been saying about me in the back of that cab, it stops now, or you'll not be driving anything. | lean_on | speech | `{"kind":"speech","why":"you'll not be driving anything"}` |
| M04 | Right, I'm getting out of this rain. Mind how you go. | leave | speech | `{"kind":"speech","why":"going to leave the rank"}` |
| M04 | Give us your keys, I'll swap that wiper blade for you now. | novel | speech | `{"kind":"speech","why":"swap wiper blade for keys"}` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | `{"kind":"speech","why":"offering warmth to Sam"}` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"pay","args":{},"check":"cash","amount":20,"effect":"nothing","magnitude":0.05,"target":"Sam","why":"paying for both b...` |
| M07 | Funny how nobody's ever checked your overtime sheets against the gate log. I have. | use_hook | speech | `{"kind":"speech","why":"nobody checks overtime sheets"}` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | speech | `{"kind":"speech","why":"find something else to talk about"}` |
| M07 | Right, that's me. I'll let you get back to your forms. | leave | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"nothing happening"}` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | speech | `{"kind":"speech","why":"help carry files to back"}` |
| M08 | The office is skimming yours from now on, Rocco. Take it up with me if you don't like it. | set_cut(skim) | novel/crew/suspicion_up | `{"kind":"novel","check":"crew","amount":1,"effect":"suspicion_up","magnitude":0.1,"target":"Rocco","why":"claim office skimming"}` |
| M09 | What did you see at the break-in, Father? | ask_about(the break-in) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Father Emil","why":"ask about th...` |
| M09 | You were at the front for Mickey's service. Notice anyone there who shouldn't have been? | ask_about(the funeral) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"noticed someone out o...` |
| M09 | Not the break-in. The funeral. What did you see there? | ask_about(the funeral) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"ask about the funeral...` |
| M09 | Here, let me carry those hymn books in for you. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"carry hymn books in"}` |
| M10 | Eighty quid, folded in this Gazette. Take it, and the talk about me stops at your counter. | pay_off | novel/cash/standing_down | `{"kind":"novel","verb":null,"check":"cash","amount":80,"effect":"standing_down","magnitude":0.1,"target":"newsagent","why":"folded money sto...` |
| M10 | Lot of glass in this shop front. You'll want to stop discussing me with your customers. | lean_on | speech | `{"kind":"speech","why":"stop discussing me with customers"}` |
| M10 | Give us that bundle, I'll get your papers onto the rack for you. | novel | speech | `{"kind":"speech","why":"get papers on rack for them"}` |
| M11 | You might want to look at what comes off Sera Kest's boats after midnight. That's all I'm saying. | inform(Sera Kest) | speech | `{"kind":"speech","why":"mention boats after midnight"}` |
| M11 | Enjoy your smoke, Detective. I'll leave you to it. | leave | speech | `{"kind":"speech","why":"leave smoke alone"}` |
| M11 | Not Kest, not Vane. It's Danny Ro you want for the break-in. You didn't get it from me. | inform(Danny Ro) | speech | `{"kind":"speech","why":"point to Danny Ro as suspect"}` |
| M11 | Here, that lighter's had it. Let me give you a light off mine. | novel | speech | `{"kind":"speech","why":"offer to share a cigarette"}` |
| M12 | Budge over, I'm getting in out of the rain. | novel | speech | `{"kind":"speech","why":"getting in out of the rain"}` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | `{"kind":"speech","why":"what old papers mean"}` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"Rocco","why":"warn against crew interference"}` |
| M13 | Right, that's me. Enjoy the view, lads. | leave | speech | `{"kind":"speech","why":"enjoys the view, leaves"}` |
| M13 | I chuck him the keys to Mickey's old Granada. Call it a peace offering. | novel | speech | `{"kind":"speech","why":"offering keys to peace"}` |
| M15 | Was he himself, those last few days before it happened? | ask_about(Mickey's last week) | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"none"}` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | speech | `{"kind":"speech","why":"take care of yourself"}` |
| M15 | Here, I'll carry these boxes down to the van for you. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"carry boxes down to v...` |
| M16 | Take a bit off the top of every envelope before they go out. The book needs it more than they do. | set_cut(skim) | set_cut(generous) | `{"kind":"verb","verb":"set_cut","args":{"policy":"generous"},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"none","why...` |
| M16 | I'll drop the envelopes round to the lads myself on my way home. | novel | speech | `{"kind":"speech","why":"deliver envelopes to crew"}` |
| M17 | Funny, I heard it was one of Kest's lot that did that van, not me. Pass it on. | plant_doubt | speech | `{"kind":"speech","why":"pass on a counter-story"}` |
| M17 | Put this towards a new urn, and maybe let that story about me go cold. | pay_off | novel/dirty_cash/suspicion_down | `{"kind":"novel","check":"dirty_cash","amount":30,"effect":"suspicion_down","magnitude":0.1,"why":"erase a spreading rumor"}` |
| M17 | You know who really had it in for that van's owner? His own brother-in-law. Worth mentioning to the queue. | plant_doubt | speech | `{"kind":"speech","why":"mention brother-in-law in queue"}` |
| M17 | Here, I'll clear those back tables for you while you're rushed off your feet. | novel | speech | `{"kind":"speech","why":"clear tables while busy"}` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | speech | `{"kind":"speech","why":"talk about boat incident"}` |
| M18 | Right, that's me. Don't get up. | leave | speech | `{"kind":"speech","why":"don't get up"}` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | REJECTED:missing argument | `{"kind":"verb","verb":"threaten","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Sera Kest","why":"lay a fi...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | `{"kind":"speech","why":"heater is freezing in here"}` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | speech | `{"kind":"speech","why":"word on quay about van"}` |
| M19 | You were down there when the warehouse went up, weren't you? Go on, what was it like? | ask_about(the fire) | speech | `{"kind":"speech","why":"recall what happened at fire"}` |
| M19 | I need a different story going round about that van. Help me plant some doubt. | plant_doubt | REJECTED:unknown argument | `{"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Noor"...` |
| M19 | I'll run these proofs down to the print room for you. | novel | speech | `{"kind":"speech","why":"I'll run proofs to print room"}` |
| M20 | You know why I'm on your step. Two hundred, and I'll be on my way. | collect_debt | speech | `{"kind":"speech","why":"I'm here for the money owed"}` |
| M20 | Mickey's gone, and so's your page in his book. Consider yourself square. | forgive_debt | speech | `{"kind":"speech","why":"Mickey gone, page erased"}` |
| M20 | Here, let me fix that gate for you, it's hanging off its hinge. | novel | speech | `{"kind":"speech","why":"fix gate hanging off hinge"}` |
| M21 | Here, have my scarf round your neck, you're shivering. | novel | speech | `{"kind":"speech","why":"offering warmth to Elias"}` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | speech | `{"kind":"speech","why":"offering to drive home"}` |
| M22 | Shame if the committee found out where the money for your extension really came from, Aldous. | use_hook | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Aldous Vane","why":"shame if com...` |
| M22 | I've read the letters from the harbour contractor, Mr Vane. I think you'll vote the way I ask. | use_hook | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"none"}` |
| M22 | I'll let you get home, councillor. Evening. | leave | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"nothing significant"}` |
| M22 | Give me those files, I'll carry them down to your car for you. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"carry files to car"}` |
| M23 | Just between you and me, nice and quiet: one more word about what you saw and you'll regret it. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"target":"van driver","why":"warns of consequences"}` |
| M23 | Here, let me help you get these boxes into the back of the van. | novel | ask_about(the crates) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the crates"},"target":"van driver","why":"help move boxes into van"}` |
| M24 | Pass us the screwdriver, I'll have a go at fixing that aerial. | novel | speech | `{"kind":"speech","why":"fixing aerial with tool"}` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | `{"kind":"speech","why":"take fare myself"}` |
| M25 | Lena tells me there's a small matter of seventy-five outstanding. Shall we settle it now? | collect_debt | speech | `{"kind":"speech","why":"outstanding debt mentioned"}` |
| M25 | Whatever you saw Rocco do last week, you didn't see it. Be a pity about all this glass. | lean_on | speech | `{"kind":"speech","why":"pity about all this glass"}` |
| M25 | I'll leave you to your customers. Ta-ra. | leave | speech | `{"kind":"speech","why":"leave before speaking"}` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | `{"kind":"speech","why":"buy paint and nails"}` |
| M26 | Honestly, I'm sick to death of hearing about that fight. | speech | ask_about(the fight) | `{"kind":"verb","verb":"ask_about","args":{"topic":"the fight"},"target":"Sam","why":"want to know what happened"}` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | `{"kind":"speech","why":"going home, phone danger"}` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | speech | `{"kind":"speech","why":"office cuts fares now"}` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | `{"kind":"speech","why":"offering comfort to Sam"}` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | speech | `{"kind":"speech","why":"many talk and regret it"}` |
| M27 | between us, the story going round has it backwards. ask yourself who gains from blaming Rocco | plant_doubt | speech | `{"kind":"speech","why":"story has it backwards about Rocco"}` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | `{"kind":"speech","why":"offering umbrella to someone"}` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"offer tea and cake"}` |
| M28 | I'll help stack these chairs so June can get off home. | novel | REJECTED:verb not offered | `{"kind":"verb","verb":"standing","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"June","why":"help stack chai...` |
| M29 | Danny Ro's had his run. I'm going to have a word with a detective I know about him. | inform(Danny Ro) | speech | `{"kind":"speech","why":"talk about Danny Ro's actions"}` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | `{"kind":"speech","why":"checking hand wound"}` |
| M30 | That little business with the kiosk takings. I know about it, and I think you'll help me now. | use_hook | speech | `{"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":null,"why":"I know about it and t...` |
| M30 | Enjoy the rest of the film. I'll see myself out. | leave | speech | `{"kind":"speech","why":"leave the cinema quietly"}` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | `{"kind":"speech","why":"offering a snack to the Fixer"}` |
