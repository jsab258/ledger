line: instrument / CI (.github/workflows/ledger-probe-unreal.yml the stage and
  copy steps; the shot line's own status word)
spec: ue-vign_camA_day.png is BYTE-IDENTICAL at run 47's probe commit and run
  48's. Run 48 did not re-render that camera, and run 47's frame is sitting
  under run 48's evidence with run 48's verdict beside it. ci.md names this
  exact fault in its own words: a run that measured nothing must say so and
  must not carry forward the previous run's files under its own name. Nothing
  in the channel says which frames a run actually produced.
acceptance: the done line carries how many of the named frames THIS run wrote,
  against how many it named, and a frame carried over from an earlier run is
  either not staged or is staged with the run that made it named on its own
  shot line
max_sessions: 1
status: READY 2026-09-16, found by an artifact-reader and re-checked by the
  resident against git rather than taken on trust.

  THE BLOB, AT FOUR REFS, WHICH IS THE WHOLE EVIDENCE:

      HEAD         20b99a41d48a88ef16158adca29117641927f44e
      c36857c0     20b99a41d48a88ef16158adca29117641927f44e   run 48's probe
      c36857c0^    20b99a41d48a88ef16158adca29117641927f44e
      bf6fc61a     20b99a41d48a88ef16158adca29117641927f44e   run 47's probe

  AND THE CONTRAST, so this is not simply a frame that renders identically:
  ue-vign_hook_day.png moved from 56b5f88188dd20ad1e69f2e61ff1f96a6da24296 at
  bf6fc61a to 5cf98288bea058c4819de398918db5203ee134a7 at c36857c0, across the
  same pair of runs. Run 48 re-rendered hook_day and did not re-render
  camA_day.

  WHY IT IS NOT HARMLESS EVEN THOUGH THE FRAME IS VALID. camA_day postdates
  the material re-pick, so as a picture it is honest evidence of the current
  materials. What is dishonest is the ATTRIBUTION: anyone comparing camA_day
  across runs 47 and 48 to ask what run 48 changed is comparing a file with
  itself and will read "no change" as a measurement. That is the null-floor
  fault with the floor removed.

  NOT YET KNOWN, AND THE ITEM MUST NOT ASSUME IT: whether the frame was never
  rendered, rendered and not copied, or rendered identically and stored as the
  same blob. The shot line for camA_day says status=WROTE, which is a claim
  about the run and not about the file, so the three cannot be told apart from
  the channel as it stands. Finding out which is the first half of the work.

  UNDER D45 a tool that measures the game: a test, no review.
