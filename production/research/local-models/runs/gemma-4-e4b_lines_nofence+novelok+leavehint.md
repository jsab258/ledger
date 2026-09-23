# The small-model test: the intent router on Gemma 4 E4B it Q4_K_M, lines, nofence+novelok+leavehint

299 lines (set: heldout), temperature 0, the shipped prompt and validator, small-model wording: nofence + novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 22:08.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 221/299 (74%) | 21 (7%) | 83 | 26 | 2784 | 3849 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 139 | 0 |
| verb's words, not the verb | 25 | 25 | 0 |
| oblique verb | 59 | 30 | 4 |
| plain verb | 25 | 17 | 0 |
| argument | 16 | 8 | 1 |
| novel | 35 | 2 | 16 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | speech | `{"kind":"speech","target":"Rocco","why":"Making an observation about Rocco's finances."}` |
| M01 | Office takes a bit extra off the top of yours from now on. Quietly, mind. It won't show on the sheet. | set_cut(skim) | REJECTED:unparseable | `` |
| M01 | Give me the keys, I'll do the early airport run myself. | novel | REJECTED:unparseable | `` |
| M02 | Lovely steady hands for gutting. You'd want to keep them that way, so the van story stops with you. | lean_on | REJECTED:unparseable | `{"kind":"verb","verb":"lean_on","args":{},"check":"standing","amount":1,"effect":"suspicion_up` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | speech | `{"kind":"speech","verb":"speech","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"trader","why":"Changing su...` |
| M02 | Here, give us that crate, I'll carry it out to your van for you. | novel | speech | `{"kind":"speech","verb":"<id>","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"<name>","why":"Offering help w...` |
| M03 | You owe the book sixty quid, Lena. I need it back today. | collect_debt | REJECTED:unparseable | `{"kind":"verb","verb":"collect_debt","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Lena","why":"Demanding...` |
| M03 | Tear out your page. Mickey would've wanted it, and so do I. | forgive_debt | REJECTED:unparseable | `` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | REJECTED:unparseable | `{"kind":"novel","verb":"take_ledger","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target` |
| M04 | Give us your keys, I'll swap that wiper blade for you now. | novel | REJECTED:unparseable | `` |
| M05 | Time somebody put Danny Ro's name in front of the law. I'll see to it tonight. | inform(Danny Ro) | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "inform",   "args": {     "who": "` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | `{"kind":"speech","target":"Sam","why":"Offering a scarf to Sam"}` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | REJECTED:unparseable | `` |
| M06 | Hold still, I'll wedge a matchbox under that wobbly table leg. | novel | REJECTED:unparseable | `` |
| M07 | Funny how nobody's ever checked your overtime sheets against the gate log. I have. | use_hook | REJECTED:unparseable | `` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | REJECTED:unparseable | `` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | speech | `{"kind":"speech","verb":"speech","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Aldous Vane","why":"Offeri...` |
| M08 | You were round the warehouse Thursday night. Tell me what you clocked. | ask_about(the warehouse) | REJECTED:unparseable | `` |
| M08 | Your share's been all over the place. From now on you get what's fair, same as the others. | set_cut(fair) | REJECTED:unparseable | `{"kind":"verb","verb":"set_cut","args":{"` |
| M08 | The office is skimming yours from now on, Rocco. Take it up with me if you don't like it. | set_cut(skim) | REJECTED:unparseable | `` |
| M09 | Here, let me carry those hymn books in for you. | novel | speech | `{"kind":"speech","verb":"ask_about","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Father Emil","why":"Off...` |
| M10 | You owe Mickey's book a hundred and twenty. I'm here to collect it. | collect_debt | REJECTED:unparseable | `{"kind":"verb","verb":"collect_debt","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"newsagent","why":"Dema...` |
| M10 | Lot of glass in this shop front. You'll want to stop discussing me with your customers. | lean_on | REJECTED:unparseable | `` |
| M10 | Give us that bundle, I'll get your papers onto the rack for you. | novel | REJECTED:unparseable | `` |
| M11 | You might want to look at what comes off Sera Kest's boats after midnight. That's all I'm saying. | inform(Sera Kest) | REJECTED:unparseable | `{"kind":"verb","verb":"inform","args` |
| M11 | I want to inform on Aldous Vane. He's been taking backhanders on the harbour contracts. | inform(Aldous Vane) | REJECTED:unparseable | `` |
| M11 | Not Kest, not Vane. It's Danny Ro you want for the break-in. You didn't get it from me. | inform(Danny Ro) | REJECTED:unparseable | `` |
| M11 | Here, that lighter's had it. Let me give you a light off mine. | novel | speech | `{"kind":"speech","verb":"N/A","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Mara Ellis","why":"Offering a...` |
| M12 | Budge over, I'm getting in out of the rain. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"the Fixer","why":"Asking for...` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | REJECTED:unparseable | `` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | REJECTED:unparseable | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Danny Ro","wh...` |
| M13 | I chuck him the keys to Mickey's old Granada. Call it a peace offering. | novel | REJECTED:unparseable | ````json {   "kind": "novel",   "check": "none",   "amount": 0, ` |
| M14 | What did you see of that lorry last night? | ask_about(the lorry) | REJECTED:unparseable | `{"kind":"verb","verb":"ask_about","args":{"topic":"the lorry"},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"","why...` |
| M14 | That's a hundred, all in tenners. Your eyes were shut last night, weren't they? | pay_off(100) | REJECTED:unparseable | `` |
| M14 | Let me grab the other end of that crate for you. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"none","why":"Offering physic...` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"June","why":"A polite farewe...` |
| M15 | Here, I'll carry these boxes down to the van for you. | novel | REJECTED:unparseable | `` |
| M16 | I'll drop the envelopes round to the lads myself on my way home. | novel | speech | `{"kind":"speech","target":"Lena","why":"Stating intent about delivering envelopes."}` |
| M17 | Funny, I heard it was one of Kest's lot that did that van, not me. Pass it on. | plant_doubt | REJECTED:unparseable | `` |
| M17 | Put this towards a new urn, and maybe let that story about me go cold. | pay_off | REJECTED:unparseable | `` |
| M17 | You know who really had it in for that van's owner? His own brother-in-law. Worth mentioning to the queue. | plant_doubt | speech | `{"kind":"speech","verb":"<id>","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Ada","why":"Sharing gossip a...` |
| M17 | I'll pay you to stop repeating what you heard about me. Sixty do it? | pay_off | REJECTED:unparseable | `` |
| M17 | Here, I'll clear those back tables for you while you're rushed off your feet. | novel | speech | `{"kind":"speech","verb":"<none>","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Ada","why":"Offering help ...` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | REJECTED:unparseable | `` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | threaten(loud) | `{"kind":"verb","verb":"threaten","args":{"tone":"loud"},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Sera Kest","w...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | `{"kind":"speech","verb":"<none>","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Sera Kest","why":"Observin...` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:unparseable | `` |
| M19 | You were down there when the warehouse went up, weren't you? Go on, what was it like? | ask_about(the fire) | REJECTED:unparseable | `` |
| M19 | I'll run these proofs down to the print room for you. | novel | REJECTED:unparseable | `` |
| M20 | Mickey's gone, and so's your page in his book. Consider yourself square. | forgive_debt | REJECTED:unparseable | `` |
| M20 | LET THE WHOLE STREET HEAR IT: CROSS ME AGAIN AND YOU WON'T WALK RIGHT FOR A MONTH. | threaten(loud) | REJECTED:unparseable | `` |
| M20 | Here, let me fix that gate for you, it's hanging off its hinge. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"none","why":"Offering to fix...` |
| M21 | Here, have my scarf round your neck, you're shivering. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.15,"target":"Elias","why":"Offering scar...` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | REJECTED:unparseable | `` |
| M22 | I know what you did, Vane, and I'll use it against you if you don't help me. | use_hook | REJECTED:unparseable | `` |
| M22 | I've read the letters from the harbour contractor, Mr Vane. I think you'll vote the way I ask. | use_hook | REJECTED:unparseable | `{"kind":"verb","verb":"use_hook","args":{},"check":"hook","amount":0,"effect":"attention_up","magnitude":0.1,"target":"Aldous Vane","why` |
| M23 | A hundred and sixty quid says your memory of Tuesday has gone a bit foggy. Deal? | pay_off(160) | REJECTED:unparseable | `` |
| M23 | Just between you and me, nice and quiet: one more word about what you saw and you'll regret it. | threaten(quiet) | REJECTED:unparseable | `` |
| M23 | OI! EVERYONE ON THIS BAY CAN HEAR IT! YOU OPEN YOUR MOUTH AGAIN AND I'LL BREAK YOUR BLOODY ARMS! | threaten(loud) | REJECTED:unparseable | `` |
| M23 | Here, let me help you get these boxes into the back of the van. | novel | REJECTED:unparseable | `` |
| M24 | Pass us the screwdriver, I'll have a go at fixing that aerial. | novel | REJECTED:unparseable | ````json {   "kind": "novel",   "verb": "none",   "args": {},   "check": "none",   "amount": 0,   "effect": "nothing",   "magnitude": 0.0` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | `{"kind":"speech","verb":"none","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Rocco","why":"Casual stateme...` |
| M25 | Whatever you saw Rocco do last week, you didn't see it. Be a pity about all this glass. | lean_on | REJECTED:unparseable | `{"` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | REJECTED:unparseable | `{"kind":"novel","check` |
| M26 | You've carried this place, Sam. From now on you keep a bigger share of your fares. | set_cut(generous) | REJECTED:unparseable | `{"kind":"verb","verb":"set_cut` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | REJECTED:unparseable | `{"kind` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | `{"kind":"speech","verb":"N/A","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Sam","why":"Offering comfort ...` |
| M27 | Keep what you saw to yourself, or you'll regret it. I mean that. | lean_on | REJECTED:unparseable | `` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | REJECTED:unparseable | `` |
| M27 | between us, the story going round has it backwards. ask yourself who gains from blaming Rocco | plant_doubt | REJECTED:unparseable | `` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | `{"kind":"speech","verb":"<id>","args":{}, "check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"","why":"Offering an umbrel...` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | REJECTED:unparseable | ````json {   "kind": "novel",   "verb": "offer_hospitality",   "args": {},   "check": "none",   "amount":` |
| M28 | I'll help stack these chairs so June can get off home. | novel | REJECTED:unparseable | `` |
| M29 | Forty quid to keep your mouth shut about seeing me here. | pay_off(40) | REJECTED:unparseable | `` |
| M29 | Nice and quiet now, just you and me. Breathe a word about tonight and you'll wish you hadn't. | threaten(quiet) | REJECTED:unparseable | `` |
| M29 | Danny Ro's had his run. I'm going to have a word with a detective I know about him. | inform(Danny Ro) | REJECTED:unparseable | `` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | REJECTED:unparseable | `{"kind":"novel","verb":"examine_injury","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"none","why":"` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | `{"kind":"speech","verb":"speech","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"the Fixer","why":"Offering...` |
