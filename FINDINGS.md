# LEDGER: open faults

Unresolved faults only, at most twenty; a fault leaves this file when fixed.
The old notebook is in production/archive/FINDINGS-to-2026-09-24.md.

- The conversation helper builds empty memory and knowledge stores and says it is day 1 on every request, so no character can answer from what the simulation knows. (Being fixed: the encounter.)
- The packaged "restart" test restores strings held in memory; it never proves a real quit and a reload from disk. (Being fixed: the encounter.)
- The new player character has no crime or conversation input; the crime key belongs to the old test character. (Being fixed: the encounter.)
- Nano cannot learn a new voice on the card: the voice encoder aborts the process on DirectML (no complex numbers). Cloning runs on the processor.
- Nano takes about four seconds to make a three-second line while the game runs, before playback begins.
- The hill's mist does not change with the fog settings; two tries had no effect.
- The ship chandler's has no name board.
- MH_Test wears the plugin's only garment, a white T-shirt and shorts, barefoot.
- The crime witness bank's line cw-ws-r4-02 has the witness saying she served the player "his bitter": alcohol, which the content rule forbids everywhere. (content/dialogue/crime-witness-v1.json)
- The local project's content import fails (38 errors, damaged packages), so a local run cannot place the witnesses on the ground and cannot prove perception; the build machine regenerates the content cleanly every run.
