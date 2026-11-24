# Reality check: reader brief (24 Nov 2026)

You are listing numbers and rules from the LEDGER blueprint (a 1990 British port-town crime game; the town Meridian, the playable map "the Hook" plus its docks, about 620 by 400 m). Root: /home/claude/ledger/production/lane/blueprint/ (git branch lane-2026-11). Never open or edit anything under ai-brain/. Do not edit any blueprint file: you only write your own CSV part.

## What to list
Every number or rule that sets something in the game or decides how the game is judged: sizes, distances, counts, spacing and density, widths, durations, speeds, prices, wages, probabilities, thresholds, timings, hours, how institutions work (police, courts, docks, Customs, shops), and every test or gate (a check that passes or fails the game). Skip: document dates, word counts, history logs, cost-of-work notes, pure story text, line wording, file housekeeping. Where one rule repeats the same value many times (e.g. 18 lamps all 30 m apart, 119 people with ages), list it once as a rule with the range or pattern, not once per item. Where the same number appears in two files, list it once and name both places.

## Columns (CSV, header exactly):
id,file_part,value_unit,what_it_sets,should_come_from,source_given,source_kind,verdict,fix,harm,note

- id: your prefix plus a number (given in your task).
- file_part: file and section or key (e.g. "BLUEPRINT-04 4.4" or "map.json lamp_columns quay_street").
- value_unit: e.g. "10 m", "120 s per game hour", "5 props per 10 m".
- what_it_sets: a few plain words.
- should_come_from: one of real-1990 (real things: sizes, distances, counts, spacing/density of street furniture, widths, how long real things take, 1990 prices, how real institutions worked; should come from 1990 Britain: dated photographs, records, standards of the period, Hansard, period trade sources) / reference-game (feel and rule numbers: how fast a watcher notices, chase lengths, fight timing, camera; from the reference games as measured) / canon (story, people, tone; canon.md, RULINGS.md, his rulings) / own-loops (everything else: our own play loops; must be marked judgement until tested).
- source_given: what the file cites, briefly (or "none").
- source_kind: the kind of that source: real-1990 / modern-real / reference-game-measured / reference-game-unmeasured / canon / ruling / own-design / own-game-built (taken from our own built prototype or scene) / memory-or-judgement / none.
- verdict: one of
  - ok: the source is the right kind and is cited.
  - wrong-source: decided by the wrong kind of thing (e.g. a real-world spacing set by a game feel need, a game-feel number taken from reality, a real number taken from our own built scene). Also use it for the reverse: reality applied where fun should decide (a real procedure or time that would make play dull); then start fix with "CHOICE FOR HIM:".
  - carried: a number taken from one setting and used in another without a check it fits (a modern standard used for 1990, a GTA VI timing used for a 1990 British constable, a US figure used for Britain, a figure for one street used for every street).
  - self-judging: a test or gate that judges the game by the game's own rules or own built content, not against an outside reference.
  - unsourced: memory, "inferred", "est.", "chosen", "judgement" or nothing, presented as settled. (A number honestly marked chosen/working/judgement and of the own-loops kind is ok, not unsourced. A real-world number marked "chosen" is unsourced.)
- fix: what should decide it instead, in a few words (e.g. "1990 BS 5489 spacing and dated photographs").
- harm: 1 to 5. 5 = the map's layout or something the one-shot build hangs on (positions, street widths, lengths, counts of map objects, anything that decides lighting and being seen); 4 = core play numbers (police, watchers, chases, clock); 3 = systems numbers (economy, routines); 2 = dressing; 1 = trivial.
- note: anything short worth saying.

Write with Python's csv module (quote fields). British spelling, no em-dashes. Plain words. Be quick: one pass through your files, judgement on each row; do not research the web. Expect roughly 100 to 400 rows for your share. When done, reply with only: the file path, the row count, and counts by verdict.
