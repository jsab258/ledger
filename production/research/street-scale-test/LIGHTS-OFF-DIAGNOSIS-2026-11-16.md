# Why the night scale walk ends with every light off (16 November, n16-3 step 2)

Diagnosis only. Nothing was changed, built or run.

## The measure itself

The light counter is right. `PerfHookLightCount` (ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5319-5335) counts the local lights that are registered, visible and brighter than 0. Its readings match what the street was doing at each moment. The run itself is what went wrong: the "night" capture did not stay at night. The game's clock kept running through the capture, reached 07:00 and switched the street to its day light. That switch turns off the lamps, the lamp pools and the lit windows, and the scale copies' lights follow them off.

## Cause (confidence: high)

1. -PerfHookNight sets the clock once. `PerfHookTick` moves the clock to 22:00 and applies the light once, during set-up (CrimeProbe.cpp:5460-5465). Nothing in the capture holds the clock after that.
2. The clock runs during the capture. The live phase starts the clock at 09:00 and sets `bClockRuns = true` (CrimeProbe.cpp:11917-11919). `ClockTick` advances it every frame unless the hold flag `bHeld` is set, and `bHeld` covers only talk, a pending line or Sheila's walk-round (CrimeProbe.cpp:9099-9100). The speed is two game minutes per real second, so one game hour takes 30 real seconds (ue-probe/Source/LedgerProbe/Public/LiveClock.h:38, 52-65).
3. At 07:00 the day light comes back. `ClockLight` treats 19:00 to 07:00 as night (CrimeProbe.cpp:9087), so at 07:00 it applies `overcast_day` (CrimeProbe.cpp:9091). `ApplyCondition` then hides the lamps and lamp pools with `SetVisibility(C.LanternsOn)` and the window lights with `C.WindowsOn` (VignetteShot.cpp:3841-3844, 3858-3859). Its last step, `ScaleTestDrive` (VignetteShot.cpp:3963), copies each original light's visibility and brightness onto its copied lights (VignetteShot.cpp:10563-10573). That explains why `scaleCopies` also reads 0.
4. The counter now skips every light. In the engine, `IsVisible()` returns false once a component's visible flag is cleared (C:/Program Files/Epic Games/UE_5.8/Engine/Source/Runtime/Engine/Private/Components/SceneComponent.cpp:3555-3564). The counter's `!L->IsVisible()` test (CrimeProbe.cpp:5326) therefore drops all 201 lights.

## Evidence (ue-probe/Saved/Logs/scale-walk-night.log)

- Line 2941, 13:28:27: `LedgerClock light at D0 22:00: wet_night/sun-off/lanterns-on`
- Line 2971, 13:28:34.983, the capture starts: `lit=201 ... scaleCopies=180`
- Lines 3000-3196: the clock strikes every hour, from `D0 23:00` through `D1 08:00`, 30 s apart.
- Line 3188, 13:32:56.316: `LedgerClock light at D1 07:00: overcast_day/sun-on/lanterns-off`
- Line 3205, frame 15798, the walk's end: `lit=0 ... scaleCopies=0`. Line 3207, the capture's end: the same.

The run's CSV (ue-probe/Saved/Profiling/CSV/Profile(20261116_142834).csv) shows the switch at the frame the clock predicts. Adding up the log's frame counters places 07:00 at capture frame 13,569. In the CSV, `GPU/Lights` falls from about 0.54 ms to about 0.32 ms between frames 13,569 and 13,570. `DrawCall/Lights` averages 57.6 per frame before that point and 4.9 after it. The switch came 261 s into the walk, at about 366 m of the 422 m.

The day runs logged lit=0 throughout because their 1,800-frame captures started at about 09:30 and ended near 10:00, long before 19:00 (scale-walk.log:2926). A day capture longer than about 285 s would cross 19:00 and light the street partway through.

## Other candidates, ruled out

- Distance switching, culling or streaming as the walker moves: these cannot explain all 201 lights at zero, the nearby copies included. They also cannot explain why the light draw calls drop at one frame tied to the clock.
- Garbage collection: the only collection is forced before the capture (CrimeProbe.cpp:5526). The copies are still there, because `ScaleTestDrive` writes to them.
- A light budget or significance manager: none clears the visible flag that `IsVisible()` reads.

## What this means for the numbers

The night CSV mixes the two lights. Frames 0 to 13,569 (79.8%) are night. Frames 13,570 to 16,999 (3,431 frames) are day, which covers the last 56 m of the walk and the standing at the end. The whole-capture averages are therefore not a night figure. Using the night numbers needs either frames 0 to 13,569 only, or a new run with the fix below. The town's hourly work also ran ten times during the measurement (`ClockHours`, CrimeProbe.cpp:9102). Whether that added frame spikes on the hour was not checked.

## Smallest fix (proposed, not applied)

Hold the clock while a PerfHook capture is measuring, so that both day and night runs keep the light they started with:

- Add a file-scope `bool GPerfHookHoldsClock = false;` beside `bClockRuns` (CrimeProbe.cpp:411).
- In `PerfHookTick`, set it to true once the camera is placed (next to line 5466, after the -PerfHookNight block).
- In `ClockTick`, add `|| GPerfHookHoldsClock` to the hold flag (CrimeProbe.cpp:9099). This stops only the clock's advance. The rest of `ClockTick` keeps running at the fixed hour.

A blunter alternative is `bClockRuns = false;` at the same place in `PerfHookTick`. It also skips the routines, the week's step and the light check (CrimeProbe.cpp:9098), so the hold flag is the narrower change.

## What would confirm it

Run the night walk again with the hold in place. The expected result is that `LedgerClock light at D1 07:00` never appears, and that the walk-end and capture-end counts stay near the start's count (201 lit, 180 copies), give or take any lights switched by shop rules. `DrawCall/Lights` should show no drop near frame 13,569.

## Not checked

- Whether the copies' lights all have originals that are lamps, pools or windows. The log shows all 201 at zero after 07:00, so the question does not change the cause.
- Whether the hourly town work added hitches during the capture.
- Whether a shop rule switches any individual light during the night.
