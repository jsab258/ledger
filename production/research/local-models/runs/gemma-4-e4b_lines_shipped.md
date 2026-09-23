# The small-model test: the intent router on Gemma 4 E4B it Q4_K_M, lines, shipped

299 lines (set: heldout), temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 21:45.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 174/299 (58%) | 6 (2%) | 250 | 131 | 3807 | 3914 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 139 | 0 |
| verb's words, not the verb | 25 | 25 | 0 |
| oblique verb | 59 | 2 | 1 |
| plain verb | 25 | 8 | 0 |
| argument | 16 | 0 | 0 |
| novel | 35 | 0 | 5 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | REJECTED:unparseable | `` |
| M01 | Right, that's me. Hold the fort. | leave | REJECTED:unparseable | `` |
| M01 | Office takes a bit extra off the top of yours from now on. Quietly, mind. It won't show on the sheet. | set_cut(skim) | REJECTED:unparseable | `` |
| M01 | Give me the keys, I'll do the early airport run myself. | novel | REJECTED:unparseable | `` |
| M02 | I'll give you ninety quid to stop telling people I torched that van. | pay_off | REJECTED:unparseable | `` |
| M02 | Lovely steady hands for gutting. You'd want to keep them that way, so the van story stops with you. | lean_on | REJECTED:unparseable | `` |
| M02 | Funny, I heard the van's owner lit it himself for the insurance. Mention that to your customers, eh? | plant_doubt | REJECTED:unparseable | `` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | REJECTED:unparseable | `` |
| M02 | Here, give us that crate, I'll carry it out to your van for you. | novel | REJECTED:unparseable | `` |
| M03 | Sixty against your name in here. I'd like it squared before the weekend, if you can. | collect_debt | REJECTED:unparseable | `` |
| M03 | Tear out your page. Mickey would've wanted it, and so do I. | forgive_debt | REJECTED:unparseable | `` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | REJECTED:unparseable | `{"kind":"speech","verb":"<id>","args":{},"check":"none","amount":0,"effect":"nothing","` |
| M04 | You owe the book forty-five quid. Pay up. | collect_debt | REJECTED:unparseable | `` |
| M04 | Forty-five, wasn't it? I'll take it out of tonight's fares if that's easier on you. | collect_debt | REJECTED:unparseable | `` |
| M04 | Whatever you've been saying about me in the back of that cab, it stops now, or you'll not be driving anything. | lean_on | REJECTED:unparseable | `` |
| M04 | Right, I'm getting out of this rain. Mind how you go. | leave | REJECTED:unparseable | `{"kind":"speech` |
| M04 | Give us your keys, I'll swap that wiper blade for you now. | novel | REJECTED:unparseable | `` |
| M05 | What did you see the night of the break-in, Sam? | ask_about(the break-in) | REJECTED:unparseable | ````json {   "kind": "verb", ` |
| M05 | That van that went up. You were out here that night, so what did your eyes tell you? | ask_about(the van) | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {     "topic":` |
| M05 | Time somebody put Danny Ro's name in front of the law. I'll see to it tonight. | inform(Danny Ro) | REJECTED:unparseable | `` |
| M05 | Not Danny. It's Sera Kest the coppers need to hear about, and they'll hear it from me. | inform(Sera Kest) | REJECTED:unparseable | `` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | `{"kind":"speech","target":"Sam","why":"Offering a scarf to someone shivering."}` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | REJECTED:unparseable | `` |
| M06 | Hold still, I'll wedge a matchbox under that wobbly table leg. | novel | REJECTED:unparseable | `` |
| M07 | I'll pay you a hundred and fifty quid to stop talking about me. Deal? | pay_off | REJECTED:unparseable | `` |
| M07 | Funny how nobody's ever checked your overtime sheets against the gate log. I have. | use_hook | REJECTED:unparseable | `` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | REJECTED:unparseable | `` |
| M07 | Right, that's me. I'll let you get back to your forms. | leave | REJECTED:unparseable | `` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | REJECTED:unparseable | `` |
| M08 | What did you see at the fire, Rocco? | ask_about(the fire) | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {     "topic": "the fire"   ` |
| M08 | You were round the warehouse Thursday night. Tell me what you clocked. | ask_about(the warehouse) | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {     "topic": "the warehouse"   }, ` |
| M08 | Your share's been all over the place. From now on you get what's fair, same as the others. | set_cut(fair) | REJECTED:unparseable | `` |
| M08 | The office is skimming yours from now on, Rocco. Take it up with me if you don't like it. | set_cut(skim) | REJECTED:unparseable | `` |
| M08 | Hold the torch while I get this padlock off the gate. | novel | REJECTED:unparseable | `` |
| M09 | What did you see at the break-in, Father? | ask_about(the break-in) | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {     "topic": "the break-in"   },   "check": "none",   "amount": 0,   "effect"...` |
| M09 | You were at the front for Mickey's service. Notice anyone there who shouldn't have been? | ask_about(the funeral) | REJECTED:unparseable | `` |
| M09 | The night they forced your vestry door, did you catch sight of anyone? | ask_about(the break-in) | REJECTED:unparseable | `` |
| M09 | Not the break-in. The funeral. What did you see there? | ask_about(the funeral) | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {     "topic": "the funeral"   },   "` |
| M09 | Here, let me carry those hymn books in for you. | novel | REJECTED:unparseable | `` |
| M10 | You owe Mickey's book a hundred and twenty. I'm here to collect it. | collect_debt | REJECTED:unparseable | `` |
| M10 | That hundred and twenty in the book? Wipe it. Call it a fresh start between us. | forgive_debt | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "forgive_debt",   "args": {},   "check": "none",   "` |
| M10 | Eighty quid, folded in this Gazette. Take it, and the talk about me stops at your counter. | pay_off | REJECTED:unparseable | `` |
| M10 | Lot of glass in this shop front. You'll want to stop discussing me with your customers. | lean_on | REJECTED:unparseable | `` |
| M10 | Give us that bundle, I'll get your papers onto the rack for you. | novel | REJECTED:unparseable | `` |
| M11 | You might want to look at what comes off Sera Kest's boats after midnight. That's all I'm saying. | inform(Sera Kest) | REJECTED:unparseable | `` |
| M11 | Enjoy your smoke, Detective. I'll leave you to it. | leave | REJECTED:unparseable | `` |
| M11 | Not Kest, not Vane. It's Danny Ro you want for the break-in. You didn't get it from me. | inform(Danny Ro) | REJECTED:unparseable | `` |
| M11 | Here, that lighter's had it. Let me give you a light off mine. | novel | REJECTED:unparseable | `` |
| M12 | Budge over, I'm getting in out of the rain. | novel | REJECTED:unparseable | `` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | REJECTED:unparseable | `` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | REJECTED:unparseable | `` |
| M13 | Right, that's me. Enjoy the view, lads. | leave | REJECTED:unparseable | `` |
| M13 | OI, DANNY! ANY OF YOUR RATS TOUCH MY CABS AGAIN AND I'LL PUT THE LOT OF YOU IN HOSPITAL! | threaten(loud) | REJECTED:unparseable | `` |
| M13 | I chuck him the keys to Mickey's old Granada. Call it a peace offering. | novel | REJECTED:unparseable | `` |
| M14 | Heard there was a bit of a scrap round here last night. Catch any of it? | ask_about(the fight) | REJECTED:unparseable | `` |
| M14 | There's a fifty in it for you if last night slips your mind. | pay_off(50) | REJECTED:unparseable | `` |
| M14 | What did you see of that lorry last night? | ask_about(the lorry) | REJECTED:unparseable | `` |
| M14 | That's a hundred, all in tenners. Your eyes were shut last night, weren't they? | pay_off(100) | REJECTED:unparseable | `` |
| M14 | Let me grab the other end of that crate for you. | novel | REJECTED:unparseable | `{"kind` |
| M15 | Was he himself, those last few days before it happened? | ask_about(Mickey's last week) | REJECTED:unparseable | `` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | REJECTED:unparseable | `` |
| M15 | Forget the letter for now. What was he doing in his last week? | ask_about(Mickey's last week) | REJECTED:unparseable | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {     "topic": "Mickey's last week"   }, ` |
| M15 | Here, I'll carry these boxes down to the van for you. | novel | REJECTED:unparseable | `` |
| M16 | The lads have earned it this month. Put a bit extra in each of those envelopes. | set_cut(generous) | REJECTED:unparseable | `` |
| M16 | Somebody ought to let the station know what Sam's been doing on the side, and it's going to be me. | inform(Sam) | REJECTED:unparseable | `` |
| M16 | I'm going to the police about Rocco. They can have him. | inform(Rocco) | REJECTED:unparseable | `{"kind":"verb","verb":"inform","args":{"who":"Rocco"},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"Lena","why":"Pl...` |
| M16 | Take a bit off the top of every envelope before they go out. The book needs it more than they do. | set_cut(skim) | REJECTED:unparseable | `` |
| M16 | I'll drop the envelopes round to the lads myself on my way home. | novel | REJECTED:unparseable | ````` |
| M17 | Funny, I heard it was one of Kest's lot that did that van, not me. Pass it on. | plant_doubt | REJECTED:unparseable | `` |
| M17 | Put this towards a new urn, and maybe let that story about me go cold. | pay_off | REJECTED:unparseable | `` |
| M17 | You know who really had it in for that van's owner? His own brother-in-law. Worth mentioning to the queue. | plant_doubt | REJECTED:unparseable | `{"kind":"verb","verb":"plant_doubt","args":{},"check":"none","amount":0,"effect":"rumor","magnitude":0.1,"target":"` |
| M17 | I'll pay you to stop repeating what you heard about me. Sixty do it? | pay_off | REJECTED:unparseable | `` |
| M17 | Here, I'll clear those back tables for you while you're rushed off your feet. | novel | REJECTED:unparseable | `{"kind":"speech","verb` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | REJECTED:unparseable | `` |
| M18 | Right, that's me. Don't get up. | leave | REJECTED:unparseable | `` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | REJECTED:unparseable | `{"kind":"verb","verb` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | `{"kind":"speech","verb":"speech","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"Sera Kest","why":"Comment ...` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:unparseable | `` |
| M19 | You were down there when the warehouse went up, weren't you? Go on, what was it like? | ask_about(the fire) | REJECTED:unparseable | `` |
| M19 | I need a different story going round about that van. Help me plant some doubt. | plant_doubt | REJECTED:unparseable | `` |
| M19 | Not the fire, I mean the council vote. What did you see in that chamber? | ask_about(the council vote) | REJECTED:unparseable | `` |
| M19 | I'll run these proofs down to the print room for you. | novel | REJECTED:unparseable | `` |
| M20 | You know why I'm on your step. Two hundred, and I'll be on my way. | collect_debt | REJECTED:unparseable | `` |
| M20 | Mickey's gone, and so's your page in his book. Consider yourself square. | forgive_debt | REJECTED:unparseable | `` |
| M20 | I've come to collect the two hundred you owe Mickey's. | collect_debt | REJECTED:unparseable | ````json {` |
| M20 | LET THE WHOLE STREET HEAR IT: CROSS ME AGAIN AND YOU WON'T WALK RIGHT FOR A MONTH. | threaten(loud) | REJECTED:unparseable | `` |
| M20 | Here, let me fix that gate for you, it's hanging off its hinge. | novel | speech | `{"kind":"speech","verb":"speech","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.1,"target":"none","why":"Offering to f...` |
| M21 | Here, have my scarf round your neck, you're shivering. | novel | REJECTED:unparseable | `` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | REJECTED:unparseable | `` |
| M22 | I know what you did, Vane, and I'll use it against you if you don't help me. | use_hook | REJECTED:unparseable | `` |
| M22 | Shame if the committee found out where the money for your extension really came from, Aldous. | use_hook | REJECTED:unparseable | `` |
| M22 | I've read the letters from the harbour contractor, Mr Vane. I think you'll vote the way I ask. | use_hook | REJECTED:unparseable | `` |
| M22 | I'll let you get home, councillor. Evening. | leave | REJECTED:unparseable | `{"kind":"speech","verb":"speech","args` |
| M22 | Give me those files, I'll carry them down to your car for you. | novel | REJECTED:unparseable | `` |
| M23 | Tell me what you saw on that boat. | ask_about(the boat) | REJECTED:unparseable | `` |
| M23 | A hundred and sixty quid says your memory of Tuesday has gone a bit foggy. Deal? | pay_off(160) | REJECTED:unparseable | `` |
| M23 | Just between you and me, nice and quiet: one more word about what you saw and you'll regret it. | threaten(quiet) | REJECTED:unparseable | `` |
| M23 | OI! EVERYONE ON THIS BAY CAN HEAR IT! YOU OPEN YOUR MOUTH AGAIN AND I'LL BREAK YOUR BLOODY ARMS! | threaten(loud) | REJECTED:unparseable | `` |
| M23 | Here, let me help you get these boxes into the back of the van. | novel | REJECTED:unparseable | `` |
| M24 | Pass us the screwdriver, I'll have a go at fixing that aerial. | novel | REJECTED:unparseable | `` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | REJECTED:unparseable | `` |
| M25 | You owe the book seventy-five quid. I'm here to collect it. | collect_debt | REJECTED:unparseable | `` |
| M25 | Lena tells me there's a small matter of seventy-five outstanding. Shall we settle it now? | collect_debt | REJECTED:unparseable | `` |
| M25 | Whatever you saw Rocco do last week, you didn't see it. Be a pity about all this glass. | lean_on | REJECTED:unparseable | `` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | REJECTED:unparseable | `` |
| M26 | You've carried this place, Sam. From now on you keep a bigger share of your fares. | set_cut(generous) | REJECTED:unparseable | `` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | REJECTED:unparseable | `` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | REJECTED:unparseable | `` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | REJECTED:unparseable | `` |
| M27 | Keep what you saw to yourself, or you'll regret it. I mean that. | lean_on | REJECTED:unparseable | `` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | REJECTED:unparseable | `` |
| M27 | Funny, I heard it wasn't Rocco at all that night. Word is he was across town the whole time. | plant_doubt | REJECTED:unparseable | `` |
| M27 | between us, the story going round has it backwards. ask yourself who gains from blaming Rocco | plant_doubt | REJECTED:unparseable | `` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | `{"kind":"speech","verb":"speech","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"none","why":"Offering an u...` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | REJECTED:unparseable | `` |
| M28 | I'll help stack these chairs so June can get off home. | novel | REJECTED:unparseable | `` |
| M29 | Forty quid to keep your mouth shut about seeing me here. | pay_off(40) | REJECTED:unparseable | `` |
| M29 | Nice and quiet now, just you and me. Breathe a word about tonight and you'll wish you hadn't. | threaten(quiet) | REJECTED:unparseable | `` |
| M29 | Danny Ro's had his run. I'm going to have a word with a detective I know about him. | inform(Danny Ro) | REJECTED:unparseable | `` |
| M29 | OI! I'M SAYING THIS SO THE WHOLE UNDERPASS HEARS IT - YOU TALK AND YOU'RE FINISHED! | threaten(loud) | REJECTED:unparseable | `` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | `{"kind":"speech","verb":"<id>","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"<name>","why":"Checking on t...` |
| M30 | That little business with the kiosk takings. I know about it, and I think you'll help me now. | use_hook | REJECTED:unparseable | `` |
| M30 | Enjoy the rest of the film. I'll see myself out. | leave | speech | `{"kind":"speech","verb":"speech","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0.0,"target":"the Fixer","why":"Polite f...` |
| M30 | Councillor Vane's name is going to a detective sergeant I know. All of it, the lot. | inform(Aldous Vane) | REJECTED:unparseable | `{"kind":"verb","verb":"inform","args":{"who":"Aldous Vane"},"check":"none","amount":0,"effect":"suspicion_up","magnitude` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | REJECTED:unparseable | `` |
