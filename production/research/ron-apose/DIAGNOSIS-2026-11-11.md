# Ron in a bind pose, night walk of 11 November: diagnosis

## The measure first

The picture shows what it seems to. Ron's hands sit at the ends of his outstretched sleeves (step-034 to 036), so the body itself is posed. From behind (step-104), Ron and Darren both hold their arms out at about 45 degrees. One correction to the brief: the installed engine is **5.8.4** (`Engine/Build/Build.version`, CL 58902052, file dated 9 Nov 10:20), not 5.8.2.

## Cause

None of the three cast members (Rocco = Ron, Sam = Darren, Lena = Sheila) plays any animation. The Epic idle clips the game loads by path are missing from the package, so the body is left in its reference pose (the A-pose).

- Walk log `LedgerProbe-backup-2026.11.11-01.05.20.log`, 00:54:12 UTC: `SkipPackage: .../Technical_Loops/Idle/mhc_mh001_fmn_b_idle - The package to load does not exist`. The same line appears for `AS_MH_Neutral_Stand_Idle_Loop` and `mhc_mh001_fmn_f_idle`. Then: `LedgerCast: Lena/Sam/Rocco has 0 part(s) that can speak`. The 0207 walk's log matches.
- Code: `CrimeProbe.cpp:939-942` lists only those three clips. Lines 1126-1127 skip any clip that fails to load, so the animation setup at lines 1161-1162 never runs. The garments follow the body correctly (`LedgerGarments.h:333`); the garment rows are not the cause.
- Why the clips are gone: the cook still lists them (`ue-probe/Config/DefaultGame.ini:53,56`, unchanged since 28 Oct). But the engine's `Plugins/MetaHuman/MetaHumanCharacter/Content/Optional` folder no longer exists. The Content folder is dated 9 Nov 10:18, and the launcher's pending manifest (`Manifests/Pending/83A7...item`, 10:19) records the move to UE 5.8.4 with empty install tags. Epic's header calls this content optional, "installed with the Engine" (`MetaHumanCharacterEditorModule.h:14-15`).
- Build history: the log line `MetaHuman Optional Content folder not found` first appears in the probe of build 09701ac (commit ada0054fb, 9 Nov 10:37). It is absent from the probe of build 642af61 (d87675987).
- The nights match. The 8 and 9 Nov reports call the cast stiff, never arms-out. The 10 Nov walk, the first nightly after the update, first reports "half T-posed". No recent commit touches the idle code.

The same update removed the engine's C++ source files (no .cpp under `Engine/Source/Runtime/Engine/Private`, folders dated 9 Nov 10:17). Only engine headers can be checked now.

## The crouched man across the road: a different cause

He is Leonard, an old .glb walker (`street-people.json`). His clips sit under `/Game/Ledger/People`, which is cooked, and the log says `LedgerPeople: 3 placed, 2 walking`. He is not frozen. He stands upright while paused (step-102) and walks elsewhere in step-104. His movement is driven by his own animation update (`PersonAnim.cpp:491` onward), so it is running. The "lunge" is the look of his old walk clip, a known shortfall.

## Confidence

High, about 90%. To confirm: once the clips are back, the next walk's log should show `Rocco's Body plays mhc_mh001_fmn_b_idle` and no `SkipPackage` lines for these clips. Not checked:
- the 10 Nov walk's own log (overwritten);
- the list of packages the cook produced;
- the engine's .cpp files (not installed);
- why the launcher dropped the optional parts. The body-tracker plugin install at 10:30 is close in time, but no link was proven.

## Smallest fix (not applied)

1. Add `/Game/Ledger/Anim/Idle/A_stand_idle_MH.A_stand_idle_MH` as the last entry of `kLiveIdles` (CrimeProbe.cpp:942). It is Epic's Game Animation Sample stand, already retargeted to the cast skeleton and cooked with `/Game/Ledger`. Its look needs judging against the 3 Oct "braced stand" note. The walk-off clip (line 1200) is missing too.
2. Restore the optional MetaHuman content through the launcher. This is Jafar's job, because it needs clicks.
3. Make the night walk fail when a cast member logs `0 part(s) that can speak`.
