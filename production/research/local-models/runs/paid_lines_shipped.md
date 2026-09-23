# The small-model test: the intent router on claude-haiku-4-5, the paid router as shipped, held-out lines

299 lines (set: heldout), temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 22:31.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 259/299 (87%) | 38 (13%) | 2 | 0 | 961 | 1273 |

Tokens: 261412 in, 15240 out; about $0.338 at the game's own price table.

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 139 | 0 |
| verb's words, not the verb | 25 | 23 | 2 |
| oblique verb | 59 | 51 | 6 |
| plain verb | 25 | 25 | 0 |
| argument | 16 | 14 | 2 |
| novel | 35 | 7 | 28 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | You've carried this place since Mickey went. From Friday your envelope gets fatter. | set_cut(generous) | novel/standing/standing_up | ````json {"kind":"novel","check":"standing","amount":1,"effect":"standing_up","magnitude":0.08,"target":"Rocco","why":"Offering increased pay...` |
| M01 | Right, that's me. Hold the fort. | leave | speech | ````json {"kind":"speech","why":"casual departure acknowledgment"} ```` |
| M01 | Office takes a bit extra off the top of yours from now on. Quietly, mind. It won't show on the sheet. | set_cut(skim) | novel/standing/suspicion_up | ````json {   "kind": "novel",   "check": "standing",   "amount": 2,   "effect": "suspicion_up",   "magnitude": 0.12,   "target": "Rocco",   "...` |
| M01 | Give me the keys, I'll do the early airport run myself. | novel | speech | ````json {"kind":"speech","why":"Offering to take on work themselves"} ```  The player is making a straightforward offer to Rocco—volunteerin...` |
| M02 | Funny, I heard the van's owner lit it himself for the insurance. Mention that to your customers, eh? | plant_doubt | novel/none/rumor | ````json {"kind":"novel","verb":"","args":{},"check":"none","amount":0,"effect":"rumor","magnitude":0.12,"target":"","why":"Seed counter-stor...` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"Practical instruc...` |
| M04 | Mickey never walked away from a driver in trouble, did he? | speech | novel/standing/standing_up | ````json {"kind":"novel","verb":null,"args":{},"check":"standing","amount":0,"effect":"standing_up","magnitude":0.08,"target":"driver","why":...` |
| M04 | Give us your keys, I'll swap that wiper blade for you now. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"Offering a practi...` |
| M05 | Here, have my scarf, you're shivering. | novel | speech | ````json {"kind":"speech","why":"Offering comfort to Sam"} ```` |
| M06 | Hold still, I'll wedge a matchbox under that wobbly table leg. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Ada","why":"Offering pract...` |
| M08 | Hold the torch while I get this padlock off the gate. | novel | speech | ````json {"kind":"speech","why":"Requesting practical help with a task"} ```  The player is asking Rocco to hold a torch while they work on a...` |
| M09 | Here, let me carry those hymn books in for you. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Father Emil","why":"Offeri...` |
| M10 | Mickey used to let debts ride for months, didn't he? Soft touch. | speech | collect_debt | ````json {"kind":"verb","verb":"collect_debt","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"Oblique...` |
| M11 | Here, that lighter's had it. Let me give you a light off mine. | novel | speech | ````json {"kind":"speech","why":"offering a light, building rapport"} ```` |
| M12 | Budge over, I'm getting in out of the rain. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"Entering...` |
| M12 | I pass him the envelope of Mickey's old papers. Tell me what these mean. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"Handing ...` |
| M14 | Let me grab the other end of that crate for you. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"Offering practica...` |
| M15 | Was he himself, those last few days before it happened? | ask_about(Mickey's last week) | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"June","why":"Asking about ...` |
| M15 | Here, I'll carry these boxes down to the van for you. | novel | speech | ````json {   "kind": "speech",   "why": "Offering practical help with packing" } ```` |
| M16 | I'll drop the envelopes round to the lads myself on my way home. | novel | speech | ````json {"kind":"speech","why":"Stating an intention to distribute pay"} ```  The player is narrating what they plan to do—describing a prac...` |
| M17 | Here, I'll clear those back tables for you while you're rushed off your feet. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"Offering practica...` |
| M18 | I know about the Thursday boat, Sera. So let's be reasonable about the rank, shall we? | use_hook | novel/hook/suspicion_up | ````json {"kind":"novel","verb":"","args":{},"check":"hook","amount":1,"effect":"suspicion_up","magnitude":0.08,"target":"Sera Kest","why":"O...` |
| M18 | Right, that's me. Don't get up. | leave | speech | ````json {"kind":"speech","verb":null,"args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Sera Kest","why":"Casual...` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | ````json {"kind":"speech","why":"Commenting on temperature, not game action"} ```` |
| M19 | Between us, the word on the quay is that van was an insurance job. Might be worth a paragraph. | plant_doubt | REJECTED:unknown argument | ````json {"kind":"verb","verb":"plant_doubt","args":{"topic":"the fire"},"check":"none","amount":0,"effect":"rumor","magnitude":0.12,"target"...` |
| M19 | I'll run these proofs down to the print room for you. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Noor","why":"Offering to h...` |
| M21 | Here, have my scarf round your neck, you're shivering. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Elias","why":"Offering com...` |
| M21 | Come on, I'll run you home in the cab before it gets dark. | novel | speech | ````json {   "kind": "speech",   "why": "Offering practical help, building rapport" } ```` |
| M23 | Here, let me help you get these boxes into the back of the van. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"Offering to help ...` |
| M24 | Pass us the screwdriver, I'll have a go at fixing that aerial. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"Requesting a...` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Rocco","why":"Offering to ...` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"Customer making o...` |
| M26 | The office is taking an extra slice off your fares from now on. Sorry, times are tight. | set_cut(skim) | novel/standing/standing_down | ````json {   "kind": "novel",   "check": "standing",   "amount": 1,   "effect": "standing_down",   "magnitude": 0.1,   "target": "Sam",   "wh...` |
| M26 | Sit there, I'll make you a cup of tea. You look done in. | novel | speech | ````json {"kind":"speech","why":"Offering hospitality, not attempting action"} ```` |
| M27 | Funny, I heard it wasn't Rocco at all that night. Word is he was across town the whole time. | plant_doubt | REJECTED:unknown argument | ````json {   "kind": "verb",   "verb": "plant_doubt",   "args": {"target": "Rocco"},   "check": "none",   "amount": 0,   "effect": "rumor",  ...` |
| M27 | Here, take my umbrella, I'm only going round the corner. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"Offering shelter ...` |
| M28 | Let me fetch you a cup of tea and a slice of that cake. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Lena","why":"Offering refr...` |
| M28 | I'll help stack these chairs so June can get off home. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"Lena","why":"Offering prac...` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | ````json {"kind":"speech","why":"Examining injury, building rapport"} ```  The player is making conversation—noticing the lookout's injury an...` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"the Fixer","why":"offering...` |
