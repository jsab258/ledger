# The lab: do exact targets work for LEDGER's art?

7 October 2026, 20:40 to 23:20, branch lab. The idea on trial, from AI-driven decompilation: give the AI an exact target, check every attempt automatically, keep the notes outside the AI.

**In short.** Exact, checked targets work wherever the thing is fully written down: the engine's code, a joiner's dimensioned drawing, a tailor's printed draft. They stop working where the work turns into making and taste: draping cloth, a lapel's roll, which of two sources to follow. Adopt them for engine questions, kit pieces from period drawings and clothing patterns; not for draping tailored clothes.

## 1. Unreal's own code, for two of the builder's problems: worked

- **Sky light:** the engine copies the sky into the street's light without loss. The street is lit at 41% of the sky you see because of our own setting. Walls and faces lose more because they see half a sky, the engine's default black lower sky, and the street's walls. The code backs the builder's own "one sky" fix.
- **Outfit Asset:** it picks one stored size and stretches it to the new body. A saved MetaHuman character bakes every outfit into a plain mesh and drops its cloth movement.
- **Cost:** about 30 minutes, plus an 11-minute helper. **Adopt: yes**, for any "why does the engine do this" question, before tuning. (Epic's GitHub refused the clone; the same 5.8.2 code is installed on your PC and answered.)

## 2. One sash window: worked, with two conditions

- Built from George Ellis's *Modern Practical Joinery* (1902). It matches its target within 1.4 mm in five drawings and ten dimensions, after two attempts.
- **The check catches the builder's errors but not the reader's.** The automatic check caught every building error. It missed four of my misreadings, because I wrote both the target and the model; a fresh reviewer found three of them in one look at the photographs. After fixes, a second fresh reviewer passed it on narrow points.
- **The rest is a choice of source.** The main point left is that Ellis's London window shows ¾ inch of frame round the glass, while the original windows photographed show 2½ to 3 inches.
- **Cost:** about an hour, plus 1½ hours of a helper finding sources, plus two reviews. **Adopt: yes, for kit pieces that period books draw** (windows, doors, shopfronts, railings), on two conditions: someone other than the builder writes the target, and you choose when the books and the photographs disagree.
- **Found:** the street's windows (1.50 m) are shorter than every period example (1.68 m).

## 3. One jacket: worked for the pattern, not for the jacket

- **The pattern is exact.** Thornton's *Standard Lounge Coat* (about 1911) was drafted by code for Ron. It reproduces every worked value printed in the book, every rule, and the book's own drawing to 0.15 inch. The checks caught four errors on the way.
- **The drape failed.** Draped on Ron in Blender, it took eleven runs to get a jacket that stays on. It failed its fresh review broadly: it reads as a loose smock.
- **The lapel does not hold.** Three different ways were tried; none gave a turned lapel with a notch.
- **Cost:** about an hour, plus 1½ hours of helpers, plus eleven short simulation runs. **Adopt: the pattern drafting, yes; draping tailored jackets in Blender, no.** Untested idea: model the jacket and check its outline against the drafted pattern, the way the window was checked.

## 4. Ron's plain clothes, modelled to a pattern (8 October): the checks worked, the clothes did not

- A fresh helper drafted Thornton's stout trousers and a crew-neck jumper for Ron and wrote the outline target. The garments were modelled on him, with no cloth simulation:
  - no body point shows through either garment;
  - the trousers' outline is within 1 cm in every view, the jumper's within 11.3 mm;
  - 3 of 22 seams match within 1 cm.
- Testing the target against Ron's body and its own pattern found seven faults in it, all fixed by its writer.
- **The fresh review failed it:** "the sleeves look like skin, and the trousers look like tracksuit bottoms". Most of the faults come from the target's own choices (the pattern's thin ease on Ron's forearm, straight wide legs with no break); an outline check cannot see them.
- **Cost:** 1 hour 31 minutes, plus 86 minutes of helpers and a 4-minute review.
- **Adopt:** not as a way to make clothes. Yes for the body check (count the body points through a garment; gate on zero), and yes for testing a target against the body and its pattern before building to it.
- Page: 4-plain-clothes/REPORT.md, https://claude.ai/artifact/5rTRS2pewmoWbjXgcPLiPo

## 8 October, afternoon: two answers for the builder, and the front door

- **The wet road's near-white mirror** (ROAD-NOTES.md, 12 minutes): our wet film is optically a sheet of water, and the engine renders it so. A real wet road is only partly under unbroken water, and the Hook sheet asks for 0.41 to 0.60 of today's reflection. The change: one "film specular" value of about 0.13 on the wet asphalt, which halves every reflection and keeps them sharp. The notes give the target per view, with each cause cited in our code and the engine's.
- **The shop glass's stair steps** (GLASS-NOTES.md, 7 minutes): the window's picture of the street is taken without anti-aliasing at 512. 1024 was clean but grew the editor's memory past 10 GB; one capture setting exists for exactly that. The fix: that setting, and 1024 for the two hero windows, with the light unchanged.
- **The four-panel front door** (5-front-door/NOTES.md, for phase 2, not the builder):
  - A fresh helper wrote the target from Ellis and a photograph, the photograph winning nine disagreements, and tested it against its own sources (68 of 69).
  - Built by script, it passes every check at the second run, and both fresh reviewers found its proportions right within about 1%.
  - Both failed it on detail the target did not write down: the mouldings' profiles, the ironmongery, and the frame's square edges and projecting transom that its own photographs show. Set aside after two tries.
  - The repository's size guard keeps the door's .glb out of git (models only where the game's build imports from), so it stays on F:, and the scripts rebuild it.

## What needs you

1. **Lab pushes:** done (allowed 8 October).
2. **Epic's code (optional):** to clone Epic's code from GitHub, accept the EpicGames invitation on GitHub, on the account this PC uses. Not needed for these answers.
3. **The street's windows: the book or the photographs?** (A, recommended) The photographed originals, 2½ to 3 inches of frame. (B) Ellis's ¾ inch.

The detail behind each test is in production/lab (NOTES.md in each folder); pictures are in production/previews/lab.

Published as a private page: https://claude.ai/artifact/GAgntnYAoqJVR6irjqjeBk
