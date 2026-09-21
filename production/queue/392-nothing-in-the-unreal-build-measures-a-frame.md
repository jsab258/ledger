line: engine and instruments (rides the slice's own dispatches, no extra runner time)
spec: Jafar, 2026-09-21: "Nothing in the Unreal build measures a frame:
  the file called FrameStats measures screenshot brightness, and the only
  frame instrument was in the Unity build D16 retired. Phase 1's gate
  names a frame budget and cannot exist until something reads one. Add the
  readout to the slice's own dispatches rather than as a separate job, so
  it costs no extra runner time."

  VERIFIED AT FILING TIME: ue-probe/Source/LedgerProbe/Public/FrameStats.h
  exists and, per his description and the file's own name, reads screen
  brightness rather than a frame time or frame rate. No other file under
  ue-probe/ names a frame-time or FPS instrument (grepped at filing time).
  production/stages.md's stage 6 exit gate names "the sim holding frame
  budget at target resident count" as a phase 1 gate clause; that gate
  cannot be evaluated until this item lands.

  THE CONSTRAINT IS THE POINT: this may not become its own dispatched job.
  It must attach to a dispatch the visual slice (queue 388, 384, 389) or
  the measurements (queue 390, 391, the scale soak 351) already make,
  reading whatever frame-timing figures the engine already exposes
  (Unreal's stat unit or stat fps, or the equivalent programmatic readout)
  alongside whatever else that dispatch already captures, and printing
  them the way every other instrument in this project prints a reading:
  the statistic named, the denominator named, a cap that announces itself
  if one applies.
acceptance: a frame-time or frame-rate figure appears in the verdict
  output of an existing slice or measurement dispatch, naming which one it
  rode, with no new dispatched job created to produce it; the figure
  states what it is a statistic of, a single frame, a peak over the
  capture, or a median, matching CLAUDE.md rule 2; and a second run of the
  same dispatch produces a second reading, so the instrument is shown to
  read on every run rather than once by hand
max_sessions: 1
status: READY 2026-09-21, filed with the visual slice's order. Depends on
  a slice or measurement dispatch actually running to ride on; if none of
  queue 388, 384, 389, 390, 391 or 351 has a runner slot yet, this item
  waits rather than inventing its own dispatch. This is this week's work.
