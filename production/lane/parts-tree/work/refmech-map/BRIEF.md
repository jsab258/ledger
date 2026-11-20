# Brief: map reference mechanics onto the parts tree (20 Nov 2026)

Problem: production/research/lane/REFERENCE-MECHANICS-2026-11-20.md lists 483 gameplay mechanics of five reference games (GTA V, Sleeping Dogs, Mafia DE, KCD2, RDR2), each marked against LEDGER's design. The parts tree (production/lane/parts-tree/PARTS-TREE.json, a bill of materials of the whole game) must account for every one that is not ruled out: each must land on an existing part, become a new part, or be marked "not for LEDGER" with a reason.

Inputs (all in /home/claude/ledger):
- production/lane/parts-tree/work/refmech-map/mechanics.json: id, group, text, mark (the design mark). Map only those whose mark does NOT start with "not for LEDGER", and only your groups.
- production/lane/parts-tree/work/refmech-map/parts-index.txt: every part, indented: id | name | what | designed_in | track. Read PARTS-TREE.json for more detail on a part if needed.
- canon.md, RULINGS.md, production/lane/synthesis/DESIGN.md (sections), production/lane/synthesis/DESIGN-ADDENDUM-2026-11-20.md (A1 to A31). Project facts: Britain 1990, third person, PC; no alcohol or gambling shown or spoken of; tobacco allowed; no children anywhere; no jumping; no AI director; a car hurts badly and never kills; Tom cannot die; guns rare and late; cab fares few and chosen, no taxi-sim parts; "we don't want a gossip simulator".

For each mechanic decide one:
- "part": it is already a part (or clearly inside one). Give the most specific part id (a leaf where possible). Use this generously when the part's name or what plainly includes it.
- "new": no part covers it and it belongs in LEDGER. Give: parent (an existing non-leaf id, or a leaf id to sit beside, say which), name (short), what (one plain line), felt (true/false), track (prototype, unreal or both; gameplay logic is "both"), gameplay (true if the one-shot browser prototype would build it: a verb, a town rule, story, interface, the game's shape), and a design (two to four plain lines of how LEDGER does it, within canon, the pillars and his rulings, 1990 Britain), and one test line.
- "out": not for LEDGER, with a one-line reason citing canon, a ruling, DESIGN 18, the setting, or canon's "smallest budget" for things that feed neither the verbs nor the town's memory.
Prefer "part" over "new"; prefer merging several mechanics into one new part over many tiny ones (same "new_key" for those). Do not invent new groups. Questions for Jafar are only for canon or scope; if a mechanic truly needs his call, set "question": one line, and still decide by your recommended answer.

Write your result as JSON to production/lane/parts-tree/work/refmech-map/map-<LETTER>.json: a list of {"id","decision","part"?,"new_key"?,"new"?:{parent,name,what,felt,track,gameplay,design,test},"reason"?,"question"?}. One entry per mechanic of your groups, none skipped. Then reply with only counts (part / new / out) and the new parts' names. Plain words, no em-dashes. Do not edit any other file. Do not use the web.
