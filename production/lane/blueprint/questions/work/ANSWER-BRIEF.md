# Answerer brief: put player questions to the LEDGER blueprint

LEDGER: a third-person crime RPG, Britain 1990, the Hook district of the port town Meridian; Frank Nowak inherits a minicab office; AI townspeople who see, remember, gossip and talk live; police act on what witnesses saw. The design lives in a blueprint. Your job: answer each question in your batch against the blueprint AS IT STANDS, then propose what to do where it falls short.

## Where to look (read-only; do not edit anything in the repository)
Root: /home/claude/lane/production/lane/blueprint/
- BLUEPRINT-01-hands.md (what Frank does: moving, talking, combat 1.3, stealth, the cab), 02-town.md (the people: routines 2.1, senses 2.2, memory 2.3, gossip 2.4, witnesses 2.5, police 2.6 and RT2 parts, shops, rivals 2.10, standing 2.12, nerve and temper 2.14, the firm 2.15, economy 2.17), 03-story.md, 04-place.md, 05-looks-sound.md, 06-interface.md, 07-shape.md, 08-technical.md, 11-conflicts-and-gaps.md (known conflicts C- and gaps; a question already listed there as a gap is still "missing" or "partly", say so with its id).
- combat/COMBAT-SYSTEM.md (CS- parts; a revision may be in progress), what-if/LONG-HEAT.md (LH- parts: the long heat, arrest, remand, trial), what-if/PROPOSED-PARTS.md (P01 to P16), what-if/QUESTIONS.csv (earlier answers to W- ids: use their parts as hints, but judge against the blueprint now), temper/TEMPER-MODEL.md, economy/ECONOMY-DESIGN-2026-11-26.md, reality-check/, fifty/, hype/, data/ (JSON: people, police.json, places.json, fares.json, ties.json, routines.json and more).
- A heading map of all chapters with line numbers: /tmp/claude-0/-home-claude/2f6b63ba-01ce-5fff-86f9-e609b4dfaaa1/scratchpad/toc.txt. Use it and Grep to find the parts; read the sections you need, not whole chapters at once.
- Authority above the blueprint: canon.md and RULINGS.md (copies at /tmp/claude-0/-home-claude/2f6b63ba-01ce-5fff-86f9-e609b4dfaaa1/scratchpad/canon.md and RULINGS.md). Canon outranks everything, then his rulings. His rulings of 24 and 25 Nov include: robbery a general action, anyone, anywhere, from the start (masks through the witness rules); pulling a driver out of a car to take it (loud, reported, heavy consequences); anyone down can be searched; readable rules decide outcomes, not hidden rolls overruling a correct play; nothing ruins a playthrough (always a way back); fire can kill; holding someone overnight; a walk-out ending (leaving Meridian); PEGI 18; guns rare, after melee; a car hurts, never kills; no alcohol or gambling shown or spoken of; no children anywhere; out of scope: mounts, swimming, explosions, armour, healing items, free fast travel, scopes, ammo types; bank not robbable at release.

## For each question, decide
- verdict: one of: answered well | partly | missing | contradictory | out by his ruling ("out by his ruling" also covers canon). "answered well" means a player asking it would get a clear, fitting answer from what is written.
- parts: the part ids or section numbers that bear on it (e.g. 2.4.1; RT2-16; CS-13; LH-04; C-338), semicolon separated; "none" if none.
- answer: one plain sentence: what the game does today by the blueprint (or "nothing is written").
For partly, missing or contradictory only (leave these empty otherwise):
- proposal: one plain sentence: what the game should do. PREFER A GENERAL RULE that would answer many questions over a one-off case, and say the rule, then how it applies here.
- rule: a short name for that general rule (3 to 8 words, e.g. "Frank as a source of talk", "Any object can be used as a weapon by weight class", "Doors, keys and locks as one system"). Reuse the same rule name across your batch whenever the same rule answers more than one question.
- class: build (changes how the game is built: data structures and systems, a new verb, a new state; must close before the one-shot) or content (an animation, a number, a line, a prop; goes to the loops).
- canyou: high, medium or low: is answering it beyond what KCD2, RDR2 and GTA V let you do, and fun and fitting for this game and 1990? Add two to five words why (e.g. "high: no game does it").
- animation: none | clips (reuse of a small shared set) | one body | two bodies (new paired animation); a few words if useful.
- pass: the Monday system pass it belongs to, exactly one of: witnesses and senses | talk and gossip | people | police and justice | the cab trade | the crowd | the economy | combat | story. (Use the nearest one; world, vehicle and interface questions go to the nearest of these.)
- decision: if the proposal needs Jafar himself (violence and menace, canon, scope, money, the story), write a few words naming the decision; else empty.

## Rules for writing
Plain British English, short, no em-dashes, no italics, no tabs or line breaks inside a cell. Never put a GTA VI story spoiler anywhere. Mafia is never a reference. No alcohol, gambling or children in any proposal. Do not soften: if the blueprint is silent, say "missing".

## Output
Write a TSV file (tab separated, no header) to the path you are given, one line per question in your batch, columns in this order:
id, verdict, parts, answer, proposal, rule, class, canyou, animation, pass, decision
Every id in your batch must appear exactly once. Check the file with a short Python script (column count 11 on every line, all ids present). Reply with: counts by verdict, and your batch's general rules each with how many questions they answer (one line each).
