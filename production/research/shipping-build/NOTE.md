# The first Shipping build: what Unreal strips, and what this game may lean on (5 October 2026)

For phase 0, item 0.6 (PLAN.md: "One Shipping launch from the shortcut on his own account, first-run preparation included"). About fifteen minutes. O = opened, S = search summary only, I = inference.

## Method

The build machine packages Development with `RunUAT BuildCookRun -platform=Win64 -clientconfig=Development -cook -build -stage -pak -archive` after `tools/ue/stage_game_data.py` (.github/workflows/ledger-probe-unreal.yml, O). The Shipping build is the same command with `-clientconfig=Shipping`, archived into ue-probe/Packaged, which production/retention.json covers as a build folder (I).

## What Shipping takes away

- **Logging.** Shipping defines NO_LOGGING, so UE_LOG writes nothing; `bUseLoggingInShipping = true` in the game's Target.cs restores it, and with an installed engine that flag alone is enough (Epic forums, "Enable logging in shipping build using Installed Builds?", and unrealution.com, S). **Tried, refused (5 October, 11:09):** UBT answered "LedgerProbe modifies the values of properties: [ bUseLoggingInShipping: True != False ]. This is not allowed, as LedgerProbe has build products in common with UnrealGame": with the installed engine the target must keep a shared build environment, and a shared one cannot change the flag. The search summaries were wrong for this setup. A Shipping copy leaves no log; the game's own written files (saves, verdicts) are what an evening leaves.
- **The console.** Console commands work in a UE5 Shipping build except when built with the launcher's installed engine (Epic forums, "How to enable console command in shipping build", S). This engine is the launcher's (C:\Program Files\Epic Games\UE_5.8). The game calls console commands from five source files (CrimeProbe, LedgerProbe, MetaHumanCost, VignetteShot, WalkProbe; O). Whatever a friend's evening needs from them (the picture ladder's settings above all) is checked in the launch, not assumed.
- **Debug drawing and stats** are compiled out (I, from the engine's defines); the "?" overlay P4 met in the Development copy should be gone.

## Not established

Whether the picture ladder's settings take effect in Shipping, whether the first launch shows its shader preparation, and whether the talk program and voice start beside a Shipping copy: each is what the launch shows.
