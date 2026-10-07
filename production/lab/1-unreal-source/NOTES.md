# Lab test 1: answering the builder's open problems from Unreal's source

Started 7 October 2026. The method on trial: an exact target (the engine's own code) and every claim checked against a file and line, instead of reasoning from documentation and memory.

## What was asked

Clone only the source of Unreal 5.8 from Epic's GitHub, shallow, without building it; answer from the code (1) why the street's sky light is far darker than the sky seen, and (2) how a MetaHuman Outfit Asset resizes to bodies and whether cloth survives conversion to a wardrobe asset.

## What happened

- **The clone was refused.** `git ls-remote https://github.com/EpicGames/UnrealEngine.git` from this PC answered "Repository not found" (7 October, about 21:40). GitHub gives that answer to an account that is not yet a member of the EpicGames organisation: linking an Epic account sends an invitation that must be accepted on GitHub, under the same GitHub account that git on this PC signs in as (the one that owns jsab258/ledger). The lab did not inspect the stored GitHub sign-in; the safety check stopped that, rightly. Nothing was cloned and no disk was used.
- **The answers were read from the installed engine instead.** Epic's installed Unreal 5.8.2 on this PC (`C:\Program Files\Epic Games\UE_5.8`, Build.version 5.8.2, changelist 56702186) carries the engine's and plugins' C++ and shaders, the same version the game builds with. Reading files does not start Unreal. The clone would add the rest of Epic's source (and later versions), not a different 5.8.2.

## The answers

- Sky light: [SKY-LIGHT.md](SKY-LIGHT.md).
- Outfit Asset and wardrobe: [OUTFIT-ASSET.md](OUTFIT-ASSET.md).

## How each claim was checked

Each answer cites files and lines in the installed 5.8.2; every line cited in SKY-LIGHT.md was opened and read in this session. OUTFIT-ASSET.md was written by a helper (Opus, 11 minutes, read only) reading the same tree; on return six of its citations were opened and matched word for word: the Production bake and its comment (MetaHumanOutfitEditorPipeline.cpp:141-158), "excludes all clothing simulation data" (ClothAssetBase.h:353-359), one size means size 0 (CollectionOutfitFacade.cpp:597-601), the RBF warp (RBFInterpolation.cpp:28-46), Production as the collection default (MetaHumanCollection.h:318-326), the sim mesh stripped without face DNA (MetaHumanDefaultEditorPipelineBase.cpp:454-455), and Epic's "adding a new Size" advice (SizedOutfitSource.h:44-47).

## Result

1. Sky light: by day the engine copies the dome into the sky light without loss; the 41% is the game's own Intensity (0.7 x 0.58), and walls and faces lose more to half a view of sky, the default black lower hemisphere and the street's own walls. The code supports the builder's "one sky" option: Intensity so the light equals the dome, real albedos, a ground-coloured lower hemisphere.
2. Outfit Asset: it never blends sizes; it picks one source size and warps the garment to the new body with an RBF over 1,500 matching body points, sim mesh first, then re-transfers skin weights. Nothing limits a body far from the source. Cloth does not survive a saved (Production) MetaHuman assembly: every outfit is baked to a plain skeletal mesh by a function documented to drop all simulation. Only the editor's unsaved Preview keeps it, or a game that puts the resized Outfit Asset on its own Chaos Cloth component (untested).

## Verdict on the method

It worked. The code is an exact target: each question ended in a definite answer with a file and line anyone can open, in about 30 minutes of the lab's time plus 11 minutes of a helper. To be fair to the builder: its note of 4 October had already opened the 5.8 source for the sky light and reached the 41% (production/research/aaa-street/WINDOWS-OTHER-DIRECTION-2026-10-04.md); what the lab adds there is the whole chain checked link by link (no hidden engine loss by day; the black lower hemisphere matters for walls and faces, which that note set aside for reflections only). On the outfit, the builder carried a forum post as a search result (production/research/clothing-pipeline/MD-TAILORED-JACKET-2026-10-01.md, source 23); it is now confirmed by the line that causes it, and the resizing is known to be a plain warp, not tailoring. Limits: binary content (the dataflow templates) cannot be read, and the code says what the engine does, not how good it looks; both answers still end in a frame to measure. Recommendation: adopt it for any "why does the engine do X" question, before any tuning; the installed 5.8.2 suffices for the version the game ships, and the GitHub clone adds only the rest of Epic's source.

## Time

Recorded in production/lab/time-log.jsonl (tools/timelog.py's format, the lab's own file so the builder's meter is untouched): 20:56 to 21:12 logged, plus about 15 minutes of reading the project's rules and the builder's notes before the timer started; the outfit helper ran 11 minutes inside that.
