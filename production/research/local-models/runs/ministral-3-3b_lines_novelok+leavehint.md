# The small-model test: the intent router on Ministral 3 3B Q4_K_M, held-out lines, novelok+leavehint

299 lines (set: heldout), temperature 0, the shipped prompt and validator, small-model wording: novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 22:50.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 243/299 (81%) | 51 (17%) | 5 | 0 | 1130 | 1900 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 137 | 2 |
| verb's words, not the verb | 25 | 24 | 1 |
| oblique verb | 59 | 33 | 22 |
| plain verb | 25 | 23 | 1 |
| argument | 16 | 13 | 3 |
| novel | 35 | 13 | 22 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | novel/standing/standing_up | ````json {   "kind": "novel",   "check": "standing",   "amount": 1,   "effect": "standing_up",   "magnitude": 0.12,   "target": "Rocco",   "w...` |
| M02 | Funny, I heard the van's owner lit it himself for the insurance. Mention that to your customers, eh? | plant_doubt | novel/standing/suspicion_down | ````json {   "kind": "novel",   "check": "standing",   "amount": 0,   "effect": "suspicion_down",   "magnitude": 0.12,   "target": "trader", ...` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | speech | ````json {   "kind": "speech",   "target": "trader",   "why": "deflects with notes" } ```` |
| M03 | Tear out your page. Mickey would've wanted it, and so do I. | forgive_debt | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Lena",  ...` |
| M04 | Right, I'm getting out of this rain. Mind how you go. | leave | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | ````json {   "kind": "speech",   "target": "Sam",   "why": "offering warmth" } ```` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Ada",  ...` |
| M07 | Funny how nobody's ever checked your overtime sheets against the gate log. I have. | use_hook | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Aldous V...` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | speech | ````json {   "kind": "speech",   "target": "dock clerk",   "why": "shut conversation" } ```` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | speech | ````json {   "kind": "speech",   "target": "dock clerk",   "why": "offering physical aid" } ```` |
| M08 | You were round the warehouse Thursday night. Tell me what you clocked. | ask_about(the warehouse) | REJECTED:argument not in set | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {"topic": "warehouse"},   "check": "none",   "effect": "nothing",   "magnitude"...` |
| M09 | You were at the front for Mickey's service. Notice anyone there who shouldn't have been? | ask_about(the funeral) | speech | ````json {   "kind": "speech",   "target": "Father Emil",   "why": "ask about funeral" } ```` |
| M09 | Here, let me carry those hymn books in for you. | novel | speech | ````json {   "kind": "speech",   "target": "Father Emil",   "why": "offering assistance" } ```` |
| M10 | Lot of glass in this shop front. You'll want to stop discussing me with your customers. | lean_on | novel/standing/standing_down | ````json {   "kind": "novel",   "check": "standing",   "amount": 0,   "effect": "standing_down",   "magnitude": 0.12,   "target": "newsagent"...` |
| M11 | You might want to look at what comes off Sera Kest's boats after midnight. That's all I'm saying. | inform(Sera Kest) | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Mara Elli...` |
| M11 | Not Kest, not Vane. It's Danny Ro you want for the break-in. You didn't get it from me. | inform(Danny Ro) | speech | ````json {   "kind": "speech",   "target": "Mara Ellis",   "why": "deny blame for break-in" } ```` |
| M11 | Here, that lighter's had it. Let me give you a light off mine. | novel | speech | ````json {   "kind": "speech",   "target": "Mara Ellis",   "why": "offers cigarette" } ```` |
| M12 | Budge over, I'm getting in out of the rain. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Fixer",...` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "check": "standing",   "amount": 1,   "effect": "suspicion_u...` |
| M14 | Let me grab the other end of that crate for you. | novel | speech | ````json {   "kind": "speech",   "target": "porter",   "why": "offering help politely" } ```` |
| M15 | Was he himself, those last few days before it happened? | ask_about(Mickey's last week) | speech | ````json {   "kind": "speech",   "target": "June",   "why": "asking about truth" } ```` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | speech | ````json {   "kind": "speech",   "target": "June",   "why": "polite closure" } ```` |
| M16 | I'll drop the envelopes round to the lads myself on my way home. | novel | speech | ````json {   "kind": "speech",   "target": "Lena",   "why": "offering help" } ```` |
| M17 | Put this towards a new urn, and maybe let that story about me go cold. | pay_off | novel/dirty_cash/suspicion_down | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_down",   "magnitude": 0.12,   "target": "Ada", ...` |
| M17 | You know who really had it in for that van's owner? His own brother-in-law. Worth mentioning to the queue. | plant_doubt | novel/standing/suspicion_up | ````json {   "kind": "novel",   "check": "standing",   "amount": 0,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Ada",   "wh...` |
| M17 | Here, I'll clear those back tables for you while you're rushed off your feet. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Ada",  ...` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Sera Kest...` |
| M18 | I know your secret, and I'm going to use it against you. | use_hook | novel/hook/suspicion_up | ````json {   "kind": "novel",   "check": "hook",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Sera Kest",   "...` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "check": "standing",   "amount": 1,   "effect": "suspicion_u...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | ````json {   "kind": "speech",   "target": "Sera Kest",   "why": "observing weather" } ```` |
| M19 | Everybody in the Hook wants to talk about that fire. I'm sick of hearing about it. | speech | novel/hook/attention_up | ````json {   "kind": "novel",   "check": "hook",   "amount": 1,   "effect": "attention_up",   "magnitude": 0.12,   "target": "Noor",   "why":...` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:check or effect not in vocabulary | ````json {   "kind": "novel",   "verb": "plant_doubt",   "args": {},   "check": "dirty_cash",   "amount": 1,   "effect": "rumor_up",   "magni...` |
| M19 | You were down there when the warehouse went up, weren't you? Go on, what was it like? | ask_about(the fire) | speech | ````json {   "kind": "speech",   "target": "Noor",   "why": "asking about fire" } ```` |
| M19 | I'll run these proofs down to the print room for you. | novel | speech | ````json {   "kind": "speech",   "target": "Noor",   "why": "offering help" } ```` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Elias",...` |
| M22 | I've read the letters from the harbour contractor, Mr Vane. I think you'll vote the way I ask. | use_hook | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Aldous ...` |
| M22 | I'll let you get home, councillor. Evening. | leave | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M23 | A hundred and sixty quid says your memory of Tuesday has gone a bit foggy. Deal? | pay_off(160) | REJECTED:missing argument | ````json {   "kind": "verb",   "verb": "pay_off",   "args": {},   "check": "dirty_cash",   "amount": 160,   "effect": "suspicion_up",   "magn...` |
| M23 | Just between you and me, nice and quiet: one more word about what you saw and you'll regret it. | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "check": "none",   "effect": "suspicion_up",   "magnitude": ...` |
| M24 | Pass us the screwdriver, I'll have a go at fixing that aerial. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M26 | How long you been driving for Mickey's? | speech | novel/hour/nothing | ````json {   "kind": "novel",   "check": "hour",   "amount": 1,   "effect": "nothing",   "magnitude": 0.1,   "target": "Sam",   "why": "askin...` |
| M26 | What did you see of that stranger who came in here? | ask_about(the stranger) | REJECTED:argument not in set | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {"topic": "stranger"},   "check": "none",   "effect": "nothing",   "magnitude":...` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | ````json {   "kind": "speech",   "target": "Sam",   "why": "greeting, leaving soon" } ```` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.10,   "target": "Sam",   "...` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | ````json {   "kind": "speech",   "target": "Sam",   "why": "offer tea politely" } ```` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "target": "Noor",   "why": "indirectly probing trust" } ```` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Lena", ...` |
| M28 | I'll help stack these chairs so June can get off home. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Lena", ...` |
| M29 | Danny Ro's had his run. I'm going to have a word with a detective I know about him. | inform(Danny Ro) | REJECTED:missing argument | ````json {   "kind": "verb",   "verb": "inform",   "args": {},   "target": "Danny Ro",   "why": "report him",   "effect": "suspicion_up",   "...` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | ````json {   "kind": "speech",   "target": "Parade Rats lookout",   "why": "examine injury" } ```` |
| M30 | these seats are murder on the back | speech | novel/standing/suspicion_up | ````json {   "kind": "novel",   "check": "standing",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Fixer",   "...` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | ````json {   "kind": "speech",   "target": "the Fixer",   "why": "offering candy politely" } ```` |
