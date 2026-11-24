# lines/ (blueprint data file 10)

Made 24 Nov 2026 by the data-build wave 2 job. Every spoken or written line is a record (TECH-PLAN section 3): id, who (a people id or a speaker kind), situation, text, words, once (day, week, game or never), tokens, src. The record carries its own cool-down.

| File | What | Lines | Written | TO WRITE |
|---|---|---|---|---|
| shared-street.json | the street's shared lines by speaker kind (converted from the cloud week's bank) | 1225 | all | none |
| own-<person>.json | one file per person who keeps own lines: 60 for the twelve most seen, 30 for the rest (FIT-L01) | 58 files | 401 (Ron, Darren, Father Walsh, June) | 1890 lines over 54 people |
| directions.json | landmark direction lines for the way and chases (GV-03) | 131 | all | none |
| frank.json | Frank's approved suggested lines and the frame's fixed lines | 58 | all | none |
| story.json | story-carrying lines: the frame's sample lines, and every story bank as TO WRITE | 31 | 21 samples | 10 banks |

Rules kept: the lead is Frank (greeting.tom became greeting.frank, greeting.tommy became greeting.frankie; Tom in any text became Frank). Sheila, Alison and Ada keep the shared lines (3.6.3). Own lines once a day; shared once a week per street. Every written text passes content-words.json (checked by tools/wave2/build_lines.py).

Own lines are not mass-written here: their quality is the story lane's.
