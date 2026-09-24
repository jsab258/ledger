# LEDGER: open faults

Unresolved faults only, at most twenty; a fault leaves this file when fixed.
The old notebook is in production/archive/FINDINGS-to-2026-09-24.md.

- Nano cannot learn a new voice on the card: the voice encoder aborts the process on DirectML (no complex numbers). Cloning runs on the processor.
- Nano takes about four seconds to make a three-second line while the game runs, before playback begins.
- The hill's mist does not change with the fog settings; two tries had no effect.
- The ship chandler's has no name board.
- The cast MetaHumans (Rocco, Lena, Sam) and MH_Test wear the plugin's only garment, a white T-shirt and shorts, barefoot. Epic's own free T-shirt, jeans and hoodie on Fab would dress them plainly, but a download needs Jafar's yes.
- No street voice rides on a cast MetaHuman yet: the street's voices find people by their stand-in's actor.
- Sam, made from the Orlando preset, reads older than his card (grey at the temples).
- The crime witness bank's line cw-ws-r4-02 has the witness saying she served the player "his bitter": alcohol, which the content rule forbids everywhere. (content/dialogue/crime-witness-v1.json)
- Suspicion is decided by the C# Core inside the conversation helper; the game's C++ port still has no suspicion of its own, so nothing outside a conversation (a crowd's reaction, a refusal to serve) can use it yet.
- On the real model the lad's questioning varies from run to run: in two of six live runs he asked nothing pointed, once inventing a man with a van. Sam's card talks on the smaller model.
- A retold rumour does not carry how well its first teller saw the man, so hearsay that names the player cannot yet raise anyone's suspicion (only first-hand accounts and sightings do).
- The mesh tool's self-test fails two checks because the decision records it reads were archived on 24 September.
- The conversation rules suggest "a message left with the barman" as period detail, which sits badly with the content rule's pubs.
- In the build's scripted encounter the three residents are still archetypes (the shopkeeper, the lad, his mate); only the playable one is Lena, Sam and Rocco.
- In the playable encounter what is said is shown as the engine's debug text, which a shipping build would not show.
- No route put a donkey jacket on a MetaHuman (24 September): Fab needs a yes to download and has no donkey jacket; MetaHuman's own outfit route cannot be scripted; the built body has no torso to fit to; image-to-3D needs an NVIDIA card. (production/research/clothing-pipeline/TRIED-2026-09-24.md)
- A broken window cannot be seen: the clear pane just vanishes. Only the caption and the shout say it went (found by the AI tester).
- Any Unreal editor running on this PC, even a game started from it, blocks the build machine's build: the engine's lock refuses the compile in seconds, and the machine then tests a stale game (the red run of 1ede8879). The rule that two Unreal builds must not overlap has to cover editors too.
