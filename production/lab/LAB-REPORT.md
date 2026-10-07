# The lab's report: exact targets for LEDGER's art?

7 to 8 October 2026, branch lab. The method on trial, from AI-driven decompilation: give the AI an exact target, check every attempt automatically in small units, keep the notes outside the agent. The question: does that work for LEDGER's art, where work has so far been judged by taste alone?

## 1. Unreal's source code: two of the builder's open problems

**Worked: yes.** Both answers came straight from the engine's code, with files and lines. (Epic's GitHub refused the clone: your GitHub account here is not yet in Epic's organisation, see below; the same 5.8.2 source is installed on this PC and was used.)

- Sky light: by day the engine copies the sky into the light with no loss; the street is lit at 41% because of the game's own setting (0.7 x 0.58). Walls and faces lose more to seeing half the sky, a black "below the horizon" default and the street's walls. The fix the code supports: light equal to the sky, real brick colours, the lower half of the sky set to the ground's colour.
- Outfit Asset: it never blends sizes; it picks one and stretches it to the new body. A saved MetaHuman character bakes every outfit into a plain mesh and drops its cloth simulation; only the editor's unsaved preview keeps it.

**Cost:** about 45 minutes of the lab's time plus 11 minutes of a helper. **Adopt: yes**, for any "why does the engine do this" question, before tuning.

## 2. One sash window

(in progress)

## 3. One jacket

(in progress)

## What needs you

- To let the lab clone Epic's source from GitHub: accept the EpicGames organisation's invitation on GitHub, signed in as the account this PC uses (it owns jsab258/ledger). Not needed for these answers.
- The lab's pushes to its branch were stopped by the safety check; the work is committed on this PC only. Allow pushes to lab, or push it yourself.
