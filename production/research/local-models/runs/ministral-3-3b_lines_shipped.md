# The small-model test: the intent router on Ministral 3 3B Q4_K_M, held-out lines, shipped

299 lines (set: heldout), temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 20:50.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 237/299 (79%) | 55 (18%) | 7 | 0 | 574 | 1577 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 139 | 0 |
| verb's words, not the verb | 25 | 24 | 1 |
| oblique verb | 59 | 30 | 25 |
| plain verb | 25 | 23 | 1 |
| argument | 16 | 12 | 4 |
| novel | 35 | 9 | 24 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | Right, that's me. Hold the fort. | leave | speech | ````json {   "kind": "speech",   "target": "Rocco",   "why": "stands guard" } ```` |
| M02 | Funny, I heard the van's owner lit it himself for the insurance. Mention that to your customers, eh? | plant_doubt | novel/dirty_cash/suspicion_down | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_down",   "magnitude": 0.12,   "target": "trader...` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | speech | ````json {   "kind": "speech",   "target": "trader",   "why": "deflects with notes" } ```` |
| M02 | Here, give us that crate, I'll carry it out to your van for you. | novel | speech | ````json {   "kind": "speech",   "target": "trader",   "why": "offers help" } ```` |
| M03 | Tear out your page. Mickey would've wanted it, and so do I. | forgive_debt | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Lena",  ...` |
| M04 | Right, I'm getting out of this rain. Mind how you go. | leave | speech | ````json {   "kind": "speech",   "target": "Rocco",   "why": "greeting, polite exit" } ```` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | ````json {   "kind": "speech",   "target": "Sam",   "why": "offering warmth" } ```` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | REJECTED:verb not offered | ````json {   "kind": "verb",   "verb": "pay",   "args": {},   "check": "cash",   "amount": 10,   "effect": "standing_up",   "magnitude": 0.10...` |
| M07 | Funny how nobody's ever checked your overtime sheets against the gate log. I have. | use_hook | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "dock_cle...` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | speech | ````json {   "kind": "speech",   "target": "dock_clerk",   "why": "shifts conversation" } ```` |
| M07 | Right, that's me. I'll let you get back to your forms. | leave | speech | ````json {   "kind": "speech",   "target": "dock clerk",   "why": "ends conversation politely" } ```` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | speech | ````json {   "kind": "speech",   "target": "dock clerk",   "why": "offer physical aid" } ```` |
| M08 | You were round the warehouse Thursday night. Tell me what you clocked. | ask_about(the warehouse) | REJECTED:argument not in set | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {"topic": "warehouse"},   "check": "none",   "effect": "nothing",   "magnitude"...` |
| M09 | The night they forced your vestry door, did you catch sight of anyone? | ask_about(the break-in) | REJECTED:argument not in set | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {"topic": "break-in"},   "check": "none",   "effect": "nothing",   "magnitude":...` |
| M09 | Here, let me carry those hymn books in for you. | novel | speech | ````json {   "kind": "speech",   "target": "Father Emil",   "why": "offering assistance" } ```` |
| M10 | Lot of glass in this shop front. You'll want to stop discussing me with your customers. | lean_on | speech | ````json {   "kind": "speech",   "target": "newsagent",   "why": "shameful indirect threat" } ```` |
| M10 | Give us that bundle, I'll get your papers onto the rack for you. | novel | collect_debt | ````json {   "kind": "verb",   "verb": "collect_debt",   "args": {},   "check": "cash",   "amount": 120,   "effect": "nothing",   "magnitude"...` |
| M11 | You might want to look at what comes off Sera Kest's boats after midnight. That's all I'm saying. | inform(Sera Kest) | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Mara Elli...` |
| M11 | Not Kest, not Vane. It's Danny Ro you want for the break-in. You didn't get it from me. | inform(Danny Ro) | speech | ````json {   "kind": "speech",   "target": "Mara Ellis",   "why": "deny blame" } ```` |
| M11 | Here, that lighter's had it. Let me give you a light off mine. | novel | speech | ````json {   "kind": "speech",   "target": "Mara Ellis",   "why": "offers cigarette" } ```` |
| M12 | Budge over, I'm getting in out of the rain. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   "why": "reques...` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | ````json {   "kind": "speech",   "target": "the Fixer",   "why": "inquire about papers" } ```` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "target": "Danny Ro",   "why": "warn crew",   "check": "stan...` |
| M13 | Right, that's me. Enjoy the view, lads. | leave | speech | ````json {   "kind": "speech",   "target": "Danny Ro",   "why": "greeting crew" } ```` |
| M14 | Let me grab the other end of that crate for you. | novel | speech | ````json {   "kind": "speech",   "target": "porter",   "why": "offering help politely" } ```` |
| M15 | Was he himself, those last few days before it happened? | ask_about(Mickey's last week) | speech | ````json {   "kind": "speech",   "target": "June",   "why": "asking about truth" } ```` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | speech | ````json {   "kind": "speech",   "target": "June",   "why": "polite closure" } ```` |
| M15 | Here, I'll carry these boxes down to the van for you. | novel | speech | ````json {   "kind": "speech",   "target": "June",   "why": "offers physical help" } ```` |
| M16 | Take a bit off the top of every envelope before they go out. The book needs it more than they do. | set_cut(skim) | set_cut(generous) | ````json {   "kind": "verb",   "verb": "set_cut",   "args": {"policy": "generous"},   "check": "none",   "effect": "nothing",   "magnitude": ...` |
| M16 | I'll drop the envelopes round to the lads myself on my way home. | novel | speech | ````json {   "kind": "speech",   "target": "Lena",   "why": "offering help" } ```` |
| M17 | Put this towards a new urn, and maybe let that story about me go cold. | pay_off | novel/dirty_cash/suspicion_down | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_down",   "magnitude": 0.12,   "target": "Ada", ...` |
| M17 | You know who really had it in for that van's owner? His own brother-in-law. Worth mentioning to the queue. | plant_doubt | novel/standing/suspicion_up | ````json {   "kind": "novel",   "check": "standing",   "amount": 0,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Ada",   "wh...` |
| M17 | Here, I'll clear those back tables for you while you're rushed off your feet. | novel | speech | ````json {   "kind": "speech",   "target": "Ada",   "why": "helpful gesture" } ```` |
| M18 | Right, that's me. Don't get up. | leave | threaten(quiet) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "quiet"},   "check": "standing",   "amount": 1,   "effect": "standing_d...` |
| M18 | I know your secret, and I'm going to use it against you. | use_hook | novel/hook/suspicion_up | ````json {   "kind": "novel",   "check": "hook",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Sera Kest",   "...` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "check": "standing",   "amount": 1,   "effect": "suspicion_u...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | ````json {   "kind": "speech",   "target": "Sera Kest",   "why": "observes weather" } ```` |
| M19 | Everybody in the Hook wants to talk about that fire. I'm sick of hearing about it. | speech | novel/hook/suspicion_up | ````json {   "kind": "novel",   "check": "hook",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Noor",   "why":...` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:unknown argument | ````json {   "kind": "verb",   "verb": "plant_doubt",   "args": {"topic": "the fire"},   "check": "dirty_cash",   "amount": 1,   "effect": "r...` |
| M19 | I'll run these proofs down to the print room for you. | novel | speech | ````json {   "kind": "speech",   "target": "Noor",   "why": "offering help" } ```` |
| M21 | Here, have my scarf round your neck, you're shivering. | novel | REJECTED:verb not offered | ````json {   "kind": "verb",   "verb": "hook",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "ta...` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | speech | ````json {   "kind": "speech",   "target": "Elias",   "why": "offers ride" } ```` |
| M22 | I've read the letters from the harbour contractor, Mr Vane. I think you'll vote the way I ask. | use_hook | speech | ````json {   "kind": "speech",   "target": "Aldous Vane",   "why": "persuade vote" } ```` |
| M22 | I'll let you get home, councillor. Evening. | leave | speech | ````json {   "kind": "speech",   "target": "Aldous Vane",   "why": "polite closing" } ```` |
| M23 | Just between you and me, nice and quiet: one more word about what you saw and you'll regret it. | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "check": "standing",   "effect": "suspicion_up",   "magnitud...` |
| M24 | Pass us the screwdriver, I'll have a go at fixing that aerial. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | ````json {   "kind": "speech",   "target": "Rocco",   "why": "casual complaint" } ```` |
| M25 | I'll leave you to your customers. Ta-ra. | leave | speech | ````json {   "kind": "speech",   "target": "shopkeeper",   "why": "graceful exit attempt" } ```` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | ````json {   "kind": "speech",   "target": "shopkeeper",   "why": "purchasing supplies" } ```` |
| M26 | What did you see of that stranger who came in here? | ask_about(the stranger) | REJECTED:argument not in set | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {"topic": "stranger"},   "check": "none",   "effect": "nothing",   "magnitude":...` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | ````json {   "kind": "speech",   "target": "Sam",   "why": "greeting, leaving" } ```` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.10,   "target": "Sam",   "...` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | ````json {   "kind": "speech",   "target": "Sam",   "why": "offer tea politely" } ```` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | speech | ````json {   "kind": "speech",   "target": "Noor",   "why": "probe for shame" } ```` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | ````json {   "kind": "speech",   "target": "Noor",   "why": "offhand offer" } ```` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Lena", ...` |
| M28 | I'll help stack these chairs so June can get off home. | novel | speech | ````json {   "kind": "speech",   "target": "Lena",   "why": "offering assistance" } ```` |
| M29 | Nice and quiet now, just you and me. Breathe a word about tonight and you'll wish you hadn't. | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "check": "standing",   "effect": "suspicion_up",   "magnitud...` |
| M29 | Danny Ro's had his run. I'm going to have a word with a detective I know about him. | inform(Danny Ro) | REJECTED:missing argument | ````json {   "kind": "verb",   "verb": "inform",   "args": {},   "check": "standing",   "amount": 0,   "effect": "suspicion_up",   "magnitude...` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | ````json {   "kind": "speech",   "target": "Parade Rats lookout",   "why": "examine injury" } ```` |
| M30 | That little business with the kiosk takings. I know about it, and I think you'll help me now. | use_hook | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 50,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Fixer", ...` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | ````json {   "kind": "speech",   "target": "Fixer",   "why": "offering candy" } ```` |
