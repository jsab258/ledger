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

Each answer cites files and lines in the installed 5.8.2; every line cited in SKY-LIGHT.md was opened and read in this session. OUTFIT-ASSET.md was written by a helper reading the same tree; its citations were spot-checked on return (see the check below).

## Time

Recorded in production/lab/time-log.jsonl (tools/timelog.py's format, the lab's own file so the builder's meter is untouched).
