line: content and assets (D18 keeps tobacco; the slot is wired and empty)
spec: RAISED BY JAFAR 2026-09-21 IN THE SAME SENTENCE AS THE VIOLATIONS, and
  the batch that removed the violations did not restore it. His words: "the
  smoking clip, which D18 keeps, is the one that got dropped."

  WHAT IS TRUE NOW, measured: the only smoking clip in the library is
  `ledger/Assets/Characters/C/smoke__Smoking_2dee24f8-....fbx.rejected`. The
  `smoke` slot is LIVE in the picker with both its patterns untouched, and
  `NpcWalker` now ASKS for it at the doorway that used to ask for `drink`, so
  the consumer exists and the slot is empty.

  WHY IT WAS REJECTED, AND IT WAS NEVER A CONTENT SCREEN. The picker's motion
  screen refused it: hips travel 0.68 m against a STILL_MAX of 0.50 m for a
  standing slot. `set_aside()`'s own docstring names this clip in the 21 August
  batch. The picker's reasoning, kept because it is the right instinct: "A file
  called Smoking whose hips travel 0.68m is not a man smoking with a drift
  problem; it is a different animation under that name."

  SO THE FIX IS A RE-PICK AND NOT A RENAME. Restoring the file as it stands
  ships whatever motion that is under the name Smoking, which is the fault the
  screen exists to catch. The harvest lives on Jafar's Windows machine, so this
  is a PC job, and Mixamo needs his account and the token he supplies. NOTHING
  IS PURCHASED: a Mixamo character or animation is a download (D46, allowlist).
acceptance: the walker prints a LIVE `smoke__` clip filling the `smoke` slot,
  and that clip passes the picker's own posture and motion screens rather than
  being admitted by loosening either bound; the count of candidates examined in
  the harvest is printed beside it, so a failure to find one reads as a
  measured absence and not as a missing step
max_sessions: 1
status: READY 2026-09-21, filed by the resident on the director's ruling
  (`game-design/decision-2026-09-21-ruling-five-landings-the-sixth-site-the-settled-night-frame-and-the-neighbourhood-that-is-not-the-town.md`, section 7).
  It is NOT blocking: D17's violations are gone, which was the urgent half.

  RULED BY: the ruling above, which landed the D18 batch and filed this as the
  half his sentence asked for that the batch did not do.
