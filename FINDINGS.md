# LEDGER: open faults

Unresolved faults only, at most twenty; a fault leaves this file when fixed.
The old notebook is in production/archive/FINDINGS-to-2026-09-24.md.

- Nano cannot learn a new voice on the card: the voice encoder aborts the process on DirectML (no complex numbers). Cloning runs on the processor.
- Nano takes about four seconds to make a three-second line while the game runs, before playback begins.
- The hill's mist does not change with the fog settings; two tries had no effect.
- The ship chandler's has no name board.
- MH_Test and the unused takes still wear the plugin's T-shirt and shorts, barefoot; the playable cast (take T2) are dressed in Epic's clothes. Epic's MetaHuman sample, to compare faces against, is not yet downloaded.
- No street voice rides on a cast MetaHuman yet: the street's voices find people by their stand-in's actor.
- The cast made to the brief is a first pass. Take T2, which the game uses: Lena wears two haircuts at once, dark where the brief says greying, with her base face's eye make-up; Sam keeps his base's moustache; Rocco's face is still close to Jorge's. Take T3 swaps the haircut cleanly and drops the make-up, but with a straight dark fringe and no make-up Lena reads less British than in T2; its grey (set on the built hair materials by their own names, hairMelanin and WhiteAmount) now shows, but as streaky highlights on some hair cards rather than an even grey, worse in the mid-shot.
- 24 pre-voiced crowd recordings still say the words the content sweep of 24 September took out (sober, children, the boy); their text is updated beside them and the new lines play silent until re-rendered. (ledger/Assets/StreamingAssets/Audio/Voice, listed in commit 47d59ce3)
- Suspicion is decided by the C# Core inside the conversation helper; the game's C++ port still has no suspicion of its own, so nothing outside a conversation (a crowd's reaction, a refusal to serve) can use it yet.
- Live talk can still invent what the simulation does not know: on the real model the lad once invented a man with a van, and in two of six runs asked nothing pointed. A word-list guard was tried on 24 September and broken by the independent check (it missed the van for Rocco, whose card mentions vans, let a leading question plant a detail that became a memory, and flagged idioms like "got the sack"); it is kept off main on the branch wip/grounding-word-list. A check of claims about the event against the character's memories of it is the next attempt.
- A retold rumour does not carry how well its first teller saw the man, so hearsay that names the player cannot yet raise anyone's suspicion (only first-hand accounts and sightings do).
- The mesh tool's self-test fails two checks because the decision records it reads were archived on 24 September.
- The conversation rules suggest "a message left with the barman" as period detail, which sits badly with the content rule's pubs.
- In the build's scripted encounter the three residents are still archetypes (the shopkeeper, the lad, his mate); only the playable one is Lena, Sam and Rocco.
- No donkey jacket exists as a MetaHuman outfit yet. The outfit route itself now runs by script end to end with Epic's own packages (import, dress, build: 24 September, overnight), so what is missing is the jacket's outfit asset; Fab has none, Hunyuan3D's outputs are banned by the allowlist, and TRELLIS needs CUDA. (production/research/clothing-pipeline/TRIED-2026-09-24.md)
- Drive C: is nearly full (about 8 GB free) and the PC has 32 GB of memory: Windows' swap file grew into C: on 24 September and cannot grow further, so two heavy jobs at once (the image model, a voice model, an editor import or build) run out of memory. Heavy jobs run one at a time; big tool data lives on F: (the old SSD). A restart gives back about 1.5 GB of swap file.
- The broken window shows as scattered glass on the pavement and an empty frame; there is no crack or falling glass, and the frame's inside card shows through.
- Any Unreal editor running on this PC, even a game started from it, blocks the build machine's build: the engine's lock refuses the compile in seconds, and the machine then tests a stale game (the red run of 1ede8879). The rule that two Unreal builds must not overlap has to cover editors too.
- A spoken answer starts 6 to 9 seconds after its words appear, sentence by sentence (the first time a person speaks includes learning their voice). The voice server holds two copies of the voice model (about 5 GB of memory).
