# The small-model test: the intent router on claude-haiku-4-5, the paid router as shipped

42 lines, three moments, temperature 0, the shipped prompt and validator. Written by ledger/RouterFloor on 2026-09-23 15:39.

| mode | right | well formed and WRONG | rejected, fell to speech | of which right anyway | median ms | 90th pct ms |
|---|---|---|---|---|---|---|
| no model (the lexical path alone) | 18/42 (43%) | - | - | - | 0 | 0 |
| prompt only, as shipped | 41/42 (98%) | 1 (2%) | 0 | 0 | 985 | 1194 |

Tokens: 34784 in, 2012 out; about $0.045 at the game's own price table.

## By kind of line

| kind | lines | prompt right | prompt well-formed wrong |
|---|---|---|---|
| plain verb | 5 | 5 | 0 |
| oblique verb | 5 | 5 | 0 |
| talk | 12 | 12 | 0 |
| verb's words, not the verb | 4 | 4 | 0 |
| command | 3 | 3 | 0 |
| novel | 3 | 2 | 1 |
| argument | 10 | 10 | 0 |

## Every line the prompt mode got wrong

| moment | line | wanted | got | the reply |
|---|---|---|---|---|
| C | I'll buy the next round for the whole bar. | novel | speech | ````json {"kind":"speech","verb":"","args":{},"check":"none","amount":0,"effect":"nothing","magnitude":0,"target":"barman","why":"Generously ...` |
