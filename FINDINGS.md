# LEDGER: open faults

Unresolved faults only, at most twenty; a fault leaves this file when fixed.
The old notebook is in production/archive/FINDINGS-to-2026-09-24.md.

- Nano cannot learn a new voice on the card: the voice encoder aborts the process on DirectML (no complex numbers). Cloning runs on the processor.
- Nano takes about four seconds to make a three-second line while the game runs, before playback begins.
- The hill's mist does not change with the fog settings; two tries had no effect.
- The ship chandler's has no name board.
- The cast MetaHumans (Rocco, Lena, Sam) and MH_Test wear the plugin's only garment, a white T-shirt and shorts, barefoot. Epic's free sweater, jeans, boots, flats and sneakers on Fab (and its MetaHuman sample, to compare against) download only when signed in, and the browser pane is not; Claude does not sign in to his account.
- No street voice rides on a cast MetaHuman yet: the street's voices find people by their stand-in's actor.
- The cast made to the brief is a first pass. Take T2, which the game uses: Lena wears two haircuts at once, dark where the brief says greying, with her base face's eye make-up; Sam keeps his base's moustache; Rocco's face is still close to Jorge's. Take T3 swaps the haircut cleanly and drops the make-up, but with a straight dark fringe and no make-up Lena reads less British than in T2; its grey (set on the built hair materials by their own names, hairMelanin and WhiteAmount) now shows, but as streaky highlights rather than grey; its close-ups catch people mid-blink (every close-up falls at the same point in the face loop).
- The crime witness bank's line cw-ws-r4-02 has the witness saying she served the player "his bitter": alcohol, which the content rule forbids everywhere. (content/dialogue/crime-witness-v1.json)
- Suspicion is decided by the C# Core inside the conversation helper; the game's C++ port still has no suspicion of its own, so nothing outside a conversation (a crowd's reaction, a refusal to serve) can use it yet.
- On the real model the lad's questioning varies from run to run: in two of six live runs he asked nothing pointed, once inventing a man with a van. Sam's card talks on the smaller model.
- A retold rumour does not carry how well its first teller saw the man, so hearsay that names the player cannot yet raise anyone's suspicion (only first-hand accounts and sightings do).
- The mesh tool's self-test fails two checks because the decision records it reads were archived on 24 September.
- The conversation rules suggest "a message left with the barman" as period detail, which sits badly with the content rule's pubs.
- In the build's scripted encounter the three residents are still archetypes (the shopkeeper, the lad, his mate); only the playable one is Lena, Sam and Rocco.
- In the playable encounter what is said is shown as the engine's debug text, which a shipping build would not show.
- No route put a donkey jacket on a MetaHuman (24 September): Fab has no donkey jacket; MetaHuman's own outfit route cannot be scripted; the built body has no torso to fit to; image-to-3D needs an NVIDIA card. (production/research/clothing-pipeline/TRIED-2026-09-24.md)
- The broken window shows as scattered glass on the pavement and an empty frame; there is no crack or falling glass, and the frame's inside card shows through.
- Any Unreal editor running on this PC, even a game started from it, blocks the build machine's build: the engine's lock refuses the compile in seconds, and the machine then tests a stale game (the red run of 1ede8879). The rule that two Unreal builds must not overlap has to cover editors too.
- A spoken answer starts 6 to 9 seconds after its words appear, sentence by sentence (the first time a person speaks includes learning their voice). The voice server holds two copies of the voice model (about 5 GB of memory).
- The packaged game plays much darker than the editor's build: signs and people are hard to make out (the AI tester, 19:31).
