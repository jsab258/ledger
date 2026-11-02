# Faster packaged builds: research note, 2 November 2026

Order item n02-6-3. Research only. Web pages read 2 November 2026 as digests: wording is paraphrase unless quoted.

## Questions

1. How long does the build machine's packaged build take now, stage by stage?
2. What does each build throw away that could be kept?
3. What does Epic say about incremental cooking, the derived data cache, shaders and BuildCookRun's skip flags, and their pitfalls?
4. Which two tries would cut the most minutes with the least risk, measured and undone how?

## 1. Minutes today (last five builds)

Stages: `production/d1-probe/ue-build.txt` at commits 8bc9b8088, c87989186, 9ed243ae4, fcad65c20, 26a17dc84. Job and later steps: the runner's step clock (`C:\actions-runner-ledger\_diag\Worker_*.log`).

| Build finished | Whole job | Compile (game + editor) | Imports and materials | Cook, stage, pak, archive | Copy to played copy | Tests after |
|---|---|---|---|---|---|---|
| 2 Nov 01:59 | 29.9 | 5.9 | 7.7 | 5.6 | 1.3 | 8.8 |
| 31 Oct 02:28 | 59.1 | 7.7 | 8.8 | 24.7 | 1.2 | 15.8 |
| 30 Oct 02:09 | 39.5 | 3.8 | 7.0 | 17.6 | 1.4 | 9.0 |
| 29 Oct 21:06 | 34.0 | 3.7 | 7.8 | 11.7 | 1.2 | 8.9 |
| 29 Oct 20:14 | 35.8 | 3.7 | 2.4 | 18.6 | 1.5 | 9.0 |
| Mean | 39.7 | 5.0 | 6.8 | 15.6 | 1.3 | 10.3 |

Setup: about 0.5 minutes. Only the 2 November cook log survives (overwritten each run): code check 0.06, cook 4.40, stage 0.95 (pak about 0.45), archive 0.09 minutes. It cooked all 5,910 packages ("FULL COOK"), rebuilt 274 textures and 110 shader maps missing from the cache, and compiled 797 shader jobs (1,076 CPU-seconds).

The cook is the largest, least steady stage; on 31 October the tests also ran 7 minutes slow (a busy PC? unverified).

## 2. What each build throws away

From `.github/workflows/ledger-probe-unreal.yml`, read in full:

- **Compiled code.** Intermediate and Binaries are deleted before the build ("COLD MEANS COLD", an old measurement) and after it, so both C++ targets compile from scratch; an unchanged rebuild takes 0.03 minutes (warmBuildMinutes).
- **Cooked output.** Saved is deleted at start and end, and the cook discards its previous result anyway: Unreal's default is a full cook (`CookIncrementalDefaultIncremental=false`).
- **Imports.** The street (156 meshes), people, vehicles, 23 shop displays (3.5 minutes alone), rooms, glass and sounds are re-imported every build, changed or not.
- **Kept: the derived data cache (DDC)**, Unreal's store of compiled shaders and compressed textures: the Zen server on F: (`F:\LedgerTools\zen\Data`), shared with the editor sessions, capped at 6 GiB (`tools/ue/UserEngine.ini`). Its log today: "5.94G used, 6G soft limit". It is full and trimming.
- The checkout is not clean: copied folders keep their 22 and 27 October dates.

**The cache is too small.** Between the 31 October and 2 November builds neither the engine (installed 1 September) nor the project's config changed, yet the cook rebuilt 37 textures and 56 shader maps of Epic's own engine and plugin content, which miss only after eviction. Our content's misses (237 textures, 54 shader maps) may be eviction or the re-imports (unverified which).

Unverified: whether the cooked output, which 5.8 keeps in the same Zen server (`bUseZenStore=True` is the engine default, BaseGame.ini line 95), counts against the cap and evicts the cache during every cook.

## 3. What Epic says, and the engine's code

- **DDC** (UE 5.8 page, undated): derived data is disposable, rebuilt on a miss; Zen is the default local cache; cooked builds do not use a DDC. https://dev.epicgames.com/documentation/unreal-engine/using-derived-data-cache-in-unreal-engine
- **Zen as cooked-output store** (labelled 5.8, written for 5.4 and 5.5): Saved/Cooked keeps only a small `ue.projectstore` file; the cooked data sits in Zen beside the DDC and is evicted once that file is deleted or 14 days old. https://dev.epicgames.com/documentation/en-us/unreal-engine/using-zen-storage-server-as-cooked-output-store-for-unreal-engine
- **Content cooking** (labelled 5.8, out of date): `-iterate` cooks only out-of-date items. https://dev.epicgames.com/documentation/unreal-engine/cooking-content-in-unreal-engine . The build operations page documents no skip flags: https://dev.epicgames.com/documentation/unreal-engine/build-operations-cooking-packaging-deploying-and-running-projects-in-unreal-engine
- **Engine source settles the flags** (`AutomationTool/AutomationUtils/ProjectParams.cs`, lines 743 to 1007): `-iterate`, `-iterativecooking` and `-cookincremental` are one switch; `-iterate` also sets `-iterativedeploy`; `-skipcook` and `-skipstage` assume the old output is right; `-nocompileeditor` equals `-skipbuildeditor`. `CookCommand.Automation.cs` line 75 passes the cooker `-iterate`; with Zen on and `LegacyIterative=false` (default), `CookOnTheFlyServer.cpp` lines 10388 to 10590 make it Epic's newer dependency-tracked incremental cook. Read, not run.
- **BaseEditor.ini [CookSettings]:** only engine classes may be skipped by default; project classes need `+IncrementalClassScriptPackageAllowList=Allow,<ProjectRoot>`; changing `ProjectCookIncrementalVersion` forces one full recook.
- **Epic's forum** (Matt.Peters for Epic): in 5.5 it gained nothing (May 2025, https://forums.unrealengine.com/t/zenstore-incremental-cook-feedback/2544985); in 5.6 an unchanged recook took 24 of 28 minutes until project classes were allowed, then 5.5 (September 2025, https://forums.unrealengine.com/t/zen-incremental-cook-has-almost-as-long-a-runtime-as-a-clean-cook/2667839); "much more robust" than the old mode, best on 5.7 or later (to February 2026, https://forums.unrealengine.com/t/content-being-re-cooked-every-time-using-latest-modified-dependencies-incremental-cooking-what-is-best-practice-here/2704868). Its checker, IncrementalValidate (https://forums.unrealengine.com/t/incremental-cooking-how-to-make-use-of-incrementalcompare-xml-and-incrementalvalidate-xml/2672636), is absent from this engine.
- **Pitfalls:** a cook error can stick until a full cook, an open bug (Epic staff, April to June 2026, https://forums.unrealengine.com/t/projectpackagingsettings-busezenstore-true-cookincremental/2736573); a hidden dependency ships stale data.
- **Shaders:** no Epic page beyond the DDC one found. The engine still cooks a DirectX 11 SM5 set beside SM6 (BaseEngine.ini line 3412): 29% of the 2 November shaders.

## 4. The two tries

**Try 1: a cache big enough for the game.** First read zenserver.log's "used" lines through one build (does the cook's output fill the cap?), then raise the cap (`tools/ue/UserEngine.ini` and retention.json's line).
- Expected: cook near 5 minutes nightly; about 10 minutes saved per build on average (0 to 19).
- Measure: five builds' coldCookMinutes and cook-cold.log's counts of "Missing cached shadermap" and "missing streaming mips", against the table.
- Fall back: restore the number; Zen trims itself.
- Could go wrong: perhaps 10 GB more is needed (unverified; uncapped, it reached 12.8 GB by 28 September, `production/research/unreal-cache-cap`). F: has 19 GB free, under his 20 GB floor; the cache on C: undoes his 30 September cleanup: the space is his decision. A busy PC would shrink the saving.

**Try 2: keep compiled code.** Stop deleting Intermediate and Binaries; keep clearing Packaged and Saved. Unreal recompiles only changed files.
- Expected: compile from 5.0 to under 1 minute when no C++ changed (about 4 saved); less when it did.
- Measure: coldBuildMinutes and editorBuildMinutes (renamed) over five builds.
- Fall back: restore the two deletes.
- Could go wrong: perhaps 6 to 8 GB stays on C: (the local copy's folders: 7.7 GB; the runner's unmeasured), against the 26 September clean-up; needs a retention line. A rare stale build: one clean build.

**Not chosen now: incremental cook.** The re-imports would recook hundreds of packages anyway; it parks GBs of cooked data in a full cache; Epic is still fixing it. It follows Try 1 and imports that skip unchanged sources (about 5 to 7 minutes). Dropping DirectX 11 shaders is a hardware-floor decision.

Confidence: medium. Minutes measured; eviction causing slow cooks likely, unverified.

## Not reached

Epic's incremental-cook guide (quoted on the forum, not found); the "Cooked Data Snapshots" page; whether Zen's cap counts cooked output; cook logs before 2 November (overwritten); GitHub Actions logs (need a sign-in).
