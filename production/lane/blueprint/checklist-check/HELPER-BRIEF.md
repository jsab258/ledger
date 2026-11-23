Helper brief: match checklist items to the LEDGER blueprint (23 Nov 2026)

The problem. A 957-item list of features players expect from modern AAA games (production/research/feature-coverage/MASTER-CHECKLIST.md, written 23 Sep 2026) has never been checked item by item against the game's blueprint (424 parts, 23 Nov 2026). For each item in your share, decide whether the blueprint covers it, and if not, why not.

The game in brief: LEDGER, a single-player third-person crime RPG on Windows PC, set in a fictional British port town in October 1990. The playable map is one district (the Hook and its docks). A browser build comes first to prove the design; the Unreal engine build follows, and looks, rendering, engine and performance work is judged only there.

Files (all in /home/claude/lane):
- production/lane/blueprint/checklist-check/items.csv: all 957 items (section, section title, id, feature, where, stage). Only your sections.
- production/lane/blueprint/checklist-check/parts-index.txt: every blueprint part, one line each: id | chapter | status | title | how it works (cut). Start here.
- The full blueprint text: production/lane/blueprint/BLUEPRINT-01-hands.md to BLUEPRINT-10-shipping.md, and BLUEPRINT.md (the one-page game and the binding rules). Grep them for words in the feature before deciding "missing"; a part's full entry often holds more than the index line. Chapter 7 holds OUT-01 to OUT-13 (things his rulings leave out).
- production/lane/blueprint/checklist-check/gaps-index.txt: gaps the blueprint already lists as missing (G1 to G371).
- /tmp/claude-0/-home-claude/55bd990d-815b-5f63-8910-70f101388872/scratchpad/canon.md and RULINGS.md: canon and his rulings, which decide what is in or out.

Verdicts (exactly one per item):
- covered: a part plainly provides the feature or sets a standard or test that includes it. Name the part ids (the first token of a parts-index line, for example 1.1.3, GD-03, RT2-20, 8.12.2). If only part of the feature is there, still "covered" when the core is there, and start the note with "partly:" and say what is not.
- out: canon or a ruling excludes it. Name the line briefly, for example "RULINGS 23 Sep genre: no jump", "canon content rule: no children", "RULINGS 23 Sep: no multiplayer", "OUT-09 no minimap". Put an OUT-nn id in parts when one fits. Do not invent exclusions: if the feature belongs to a system the game seems not to have but no canon or ruling line says so, mark it missing and start the note with "Decide in or out:".
- unreal: a looks, rendering, engine, graphics-settings or performance item that the browser build skips and the Unreal build must meet. Name the blueprint parts that cover it (often status "outside"), or "none" if no part does; when "none", the note says what the blueprint would need.
- missing: nothing in the blueprint covers it and nothing excludes it. The note is one line, plain words, saying what the blueprint would need (a part, a standard or a test). If gaps-index already lists it, put the G number in the gap column.

Output: a CSV file (with a header) at the path your task names, columns: id,verdict,parts,gap,note
- parts: ids separated by spaces, or empty for missing.
- note: one short line, plain words, British spelling, no em dashes. Quote fields that contain commas.
- One row for every item in your sections, in the list's order, nothing skipped. Check the count at the end.

Be fair both ways: do not mark covered on a loose word match (a part about car doors does not cover a menu's back button); do not mark missing without grepping the full chapter files for the feature's key words. Interface and menu basics live mostly in chapters 06 and 08; saving and difficulty in 07; sound in 05; accessibility and settings in 06, 08 and 10; release, store and licences in 10; how the game is made in 09.

Your final message: the path written, the row count, and counts per verdict. Nothing else.
