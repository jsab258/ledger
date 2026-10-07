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

## What needs you

1. **Lab pushes:** the safety check stopped my pushes to the lab branch, so the work is saved on this PC only. Allow pushes to lab, or push it yourself.
2. **Epic's code (optional):** to clone Epic's code from GitHub, accept the EpicGames invitation on GitHub, on the account this PC uses. Not needed for these answers.
3. **The street's windows: the book or the photographs?** (A, recommended) The photographed originals, 2½ to 3 inches of frame. (B) Ellis's ¾ inch.

The detail behind each test is in production/lab (NOTES.md in each folder); pictures are in production/previews/lab.

Published as a private page: https://claude.ai/artifact/GAgntnYAoqJVR6irjqjeBk
