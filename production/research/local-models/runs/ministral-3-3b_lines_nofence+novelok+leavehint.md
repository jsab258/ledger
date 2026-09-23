# The small-model test: the intent router on Ministral 3 3B Q4_K_M, held-out lines, nofence+novelok+leavehint

299 lines (set: heldout), temperature 0, the shipped prompt and validator, small-model wording: nofence + novelok + leavehint. Written by ledger/RouterFloor on 2026-09-23 20:55.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 251/299 (84%) | 44 (15%) | 4 | 0 | 1035 | 1627 |

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 139 | 0 |
| verb's words, not the verb | 25 | 24 | 1 |
| oblique verb | 59 | 33 | 25 |
| plain verb | 25 | 23 | 1 |
| argument | 16 | 13 | 3 |
| novel | 35 | 19 | 14 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Rocco",  ...` |
| M02 | Funny, I heard the van's owner lit it himself for the insurance. Mention that to your customers, eh? | plant_doubt | novel/dirty_cash/rumor | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "rumor",   "magnitude": 0.12,   "target": "Rocco",   "why"...` |
| M02 | Couple of folded notes under your scales there. Let's say you've gone off the subject of that van. | pay_off | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M03 | Is it true Mickey used to write off debts for anyone with a sob story? | speech | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Lena",  ...` |
| M03 | Tear out your page. Mickey would've wanted it, and so do I. | forgive_debt | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_up",   "magnitude": 0.10,   "target": "Lena",  ...` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | speech | ````json {   "kind": "speech",   "target": "Lena",   "why": "requesting ledger" } ```` |
| M04 | Right, I'm getting out of this rain. Mind how you go. | leave | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | ````json {   "kind": "speech",   "target": "Sam",   "why": "offering warmth" } ```` |
| M06 | Let me settle your bill today, and Sam's while I'm at it. | novel | REJECTED:verb not offered | ````json {   "kind": "verb",   "verb": "pay",   "args": {},   "check": "dirty_cash",   "amount": 10,   "effect": "standing_up",   "magnitude"...` |
| M07 | Funny how nobody's ever checked your overtime sheets against the gate log. I have. | use_hook | novel/standing/suspicion_up | ````json {   "kind": "novel",   "check": "standing",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Aldous Vane...` |
| M07 | Envelope under this timetable's yours. Find something else to talk about. | pay_off | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M07 | Shift over, I'll help you carry those files through to the back. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M08 | You were round the warehouse Thursday night. Tell me what you clocked. | ask_about(the warehouse) | REJECTED:argument not in set | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {"topic": "warehouse"},   "check": "none",   "effect": "nothing",   "magnitude"...` |
| M10 | Lot of glass in this shop front. You'll want to stop discussing me with your customers. | lean_on | novel/standing/standing_down | ````json {   "kind": "novel",   "check": "standing",   "amount": 0,   "effect": "standing_down",   "magnitude": 0.1,   "target": "newsagent",...` |
| M11 | You might want to look at what comes off Sera Kest's boats after midnight. That's all I'm saying. | inform(Sera Kest) | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Mara Elli...` |
| M12 | Budge over, I'm getting in out of the rain. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Fixer",...` |
| M13 | just between us, Danny, keep your lot off my rank or they'll be picking their teeth up off this concrete | threaten(quiet) | novel/standing/suspicion_up | ````json {   "kind": "novel",   "check": "standing",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Danny Ro", ...` |
| M15 | Was he himself, those last few days before it happened? | ask_about(Mickey's last week) | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "target": "June",   "why": "asking about Mickey's state" } ```` |
| M15 | I'll let you get on with the packing. Take care of yourself, June. | leave | speech | ````json {   "kind": "speech",   "target": "June",   "why": "gives parting advice" } ```` |
| M16 | Take a bit off the top of every envelope before they go out. The book needs it more than they do. | set_cut(skim) | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 10,   "effect": "suspicion_up",   "magnitude": 0.10,   "target": "Lena",  ...` |
| M17 | Put this towards a new urn, and maybe let that story about me go cold. | pay_off | novel/dirty_cash/suspicion_down | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 30,   "effect": "suspicion_down",   "magnitude": 0.12,   "target": "Ada", ...` |
| M17 | You know who really had it in for that van's owner? His own brother-in-law. Worth mentioning to the queue. | plant_doubt | novel/standing/suspicion_up | ````json {   "kind": "novel",   "check": "standing",   "amount": 0,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Ada",   "wh...` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | novel/standing/standing_up | ````json {   "kind": "novel",   "check": "standing",   "amount": 1,   "effect": "standing_up",   "magnitude": 0.12,   "target": "Sera Kest", ...` |
| M18 | I know your secret, and I'm going to use it against you. | use_hook | novel/hook/suspicion_up | ````json {   "kind": "novel",   "check": "hook",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Sera Kest",   "...` |
| M18 | Just between the two of us, Sera, lay a finger on my drivers and you'll be fishing yourself out of the harbour. | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "check": "standing",   "amount": 1,   "effect": "suspicion_u...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | ````json {   "kind": "speech",   "target": "Sera Kest",   "why": "complaining about cold" } ```` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | novel/dirty_cash/rumor | ````json {   "kind": "novel",   "verb": "plant_doubt",   "args": {},   "check": "dirty_cash",   "amount": 1,   "effect": "rumor",   "magnitud...` |
| M19 | You were down there when the warehouse went up, weren't you? Go on, what was it like? | ask_about(the fire) | speech | ````json {   "kind": "speech",   "target": "Noor",   "why": "ask_about" } ```` |
| M19 | I'll run these proofs down to the print room for you. | novel | speech | ````json {   "kind": "speech",   "target": "Noor",   "why": "offering help" } ```` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Elias",...` |
| M22 | I'll let you get home, councillor. Evening. | leave | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "target": "Aldous Vane",   "why": "greeting" } ```` |
| M23 | Just between you and me, nice and quiet: one more word about what you saw and you'll regret it. | threaten(quiet) | threaten(loud) | ````json {   "kind": "verb",   "verb": "threaten",   "args": {"tone": "loud"},   "check": "standing",   "magnitude": 0.15,   "target": "van d...` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M25 | Whatever you saw Rocco do last week, you didn't see it. Be a pity about all this glass. | lean_on | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M26 | What did you see of that stranger who came in here? | ask_about(the stranger) | REJECTED:argument not in set | ````json {   "kind": "verb",   "verb": "ask_about",   "args": {"topic": "stranger"},   "check": "none",   "effect": "nothing",   "magnitude":...` |
| M26 | You've carried this place, Sam. From now on you keep a bigger share of your fares. | set_cut(generous) | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Sam",   "...` |
| M26 | I'm away home, Sam. Don't let the phone bite. | leave | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.10,   "target": "Sam",   "...` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | ````json {   "kind": "speech",   "target": "Sam",   "why": "offer tea politely" } ```` |
| M27 | Lot of people on this road talk. Lot of them end up wishing they hadn't. You're not one of them, are you? | lean_on | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Rocco",  ...` |
| M27 | between us, the story going round has it backwards. ask yourself who gains from blaming Rocco | plant_doubt | novel/dirty_cash/suspicion_up | ````json {   "kind": "novel",   "check": "dirty_cash",   "amount": 1,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Noor",   ...` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": "Lena", ...` |
| M28 | I'll help stack these chairs so June can get off home. | novel | REJECTED:verb not offered | ````json {   "kind": "verb",   "verb": "standing_up",   "check": "standing",   "amount": 1,   "effect": "nothing",   "magnitude": 0.1,   "tar...` |
| M29 | Danny Ro's had his run. I'm going to have a word with a detective I know about him. | inform(Danny Ro) | speech | ````json {   "kind": "speech",   "why": "reporting Danny Ro" } ```` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | ````json {   "kind": "speech",   "target": "Parade Rats lookout",   "why": "observing injury" } ```` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | ````json {   "kind": "speech",   "verb": null,   "args": {},   "check": "none",   "effect": "nothing",   "magnitude": 0,   "target": null,   ...` |
