# LEDGER: open faults

Unresolved faults only, at most twenty; a fault leaves this file when fixed.
The old notebook is in production/archive/FINDINGS-to-2026-09-24.md.

- Nano cannot learn a new voice on the card: the voice encoder aborts the process on DirectML (no complex numbers). Cloning runs on the processor.
- Nano takes about four seconds to make a three-second line while the game runs, before playback begins.
- The hill's mist does not change with the fog settings; two tries had no effect.
- The ship chandler's has no name board.
- MH_Test wears the plugin's only garment, a white T-shirt and shorts, barefoot.
- The crime witness bank's line cw-ws-r4-02 has the witness saying she served the player "his bitter": alcohol, which the content rule forbids everywhere. (content/dialogue/crime-witness-v1.json)
- Suspicion is not ported to the game's C++ and is not sent to the conversation helper, so a live character who knows about a crime has no reason to question the player. In the encounter the questioning is proven only with the stand-in model; the live model, given the lad's real memory, talked about the window job and asked nothing.
- The encounter's lad is answered through Sam's character card: the crime's residents are archetypes with no cards.
- The encounter runs only as a test mode of the crime module; the ordinary playable slice does not yet start the conversation helper, shout or save.
