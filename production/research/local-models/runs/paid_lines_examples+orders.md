# The small-model test: the intent router on claude-haiku-4-5, the paid router, lines, examples+orders

299 lines (set: heldout), temperature 0, the shipped prompt and validator, 6 worked examples per line from 225. Written by ledger/RouterFloor on 2026-09-24 07:37.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 165/299 (55%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 286/299 (96%) | 12 (4%) | 1 | 0 | 713 | 1086 |

Tokens: 331519 in, 9508 out; about $0.379 at the game's own price table.

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| talk | 139 | 138 | 1 |
| verb's words, not the verb | 25 | 24 | 1 |
| oblique verb | 59 | 55 | 3 |
| plain verb | 25 | 25 | 0 |
| argument | 16 | 16 | 0 |
| novel | 35 | 28 | 7 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| M01 | Right, that's me. Hold the fort. | leave | speech | ````json {"kind":"speech","why":"Casual farewell, no action requested"} ```` |
| M03 | Pass me the ledger, I'm locking it in the safe tonight. | novel | speech | ````json {"kind":"speech"} ```` |
| M04 | Mickey never walked away from a driver in trouble, did he? | speech | collect_debt | ````json {"kind":"verb","verb":"collect_debt","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"","why":"Invokin...` |
| M11 | Here, that lighter's had it. Let me give you a light off mine. | novel | speech | ````json {"kind":"speech","why":"offering a practical kindness"} ```` |
| M15 | Was he himself, those last few days before it happened? | ask_about(Mickey's last week) | speech | ````json {"kind":"speech"} ```  The player is asking June a genuine question about Mickey's state of mind in his final days—whether he seemed...` |
| M18 | Right, that's me. Don't get up. | leave | speech | ````json {"kind":"speech","why":"casual greeting, no action attempted"} ```` |
| M18 | I'm switching that heater on, it's freezing in here. | novel | speech | ````json {"kind":"speech"} ```` |
| M24 | I'll take the next fare myself. You put your feet up. | novel | speech | ````json {"kind":"speech","why":"offering to take work, casual kindness"} ```  The player is making a straightforward offer to do something h...` |
| M25 | I'll take a tin of that green paint and a box of nails, please. | novel | speech | ````json {"kind":"speech","why":"Ordinary customer transaction request"} ```` |
| M26 | Heard from Lena at all today? | speech | ask_about(the stranger) | ````json {"kind":"verb","verb":"ask_about","args":{"topic":"the stranger"},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target...` |
| M27 | Funny, I heard it wasn't Rocco at all that night. Word is he was across town the whole time. | plant_doubt | REJECTED:unknown argument | ````json {"kind":"verb","verb":"plant_doubt","args":{"target":"Rocco"},"check":"none","amount":0,"effect":"rumor","magnitude":0.1,"target":"R...` |
| M29 | Hold still, let me have a look at that cut on your hand. | novel | speech | ````json {"kind":"speech","why":"Offering first aid, not transacting"} ```` |
| M30 | Here, I brought you a choc ice from the kiosk. Go on, take it. | novel | speech | ````json {"kind":"speech"} ```  The player is offering the Fixer a gift—a friendly gesture, a small courtesy. This is genuine conversation, n...` |
